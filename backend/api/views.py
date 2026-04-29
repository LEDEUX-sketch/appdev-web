import csv
import jwt
from django.conf import settings
from django.db import transaction
from django.db.models import Q, Count
from django.db.models.functions import TruncHour
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from .models import Election, Position, Partylist, Candidate, Voter, VoteRecord
from .serializers import (
    ElectionSerializer, PositionSerializer, PartylistSerializer,
    CandidateSerializer, VoterSerializer, VoterListSerializer,
    VoteRecordSerializer, SubmitVoteSerializer
)


class VoterLoginThrottle(AnonRateThrottle):
    """Limits anonymous voter login attempts to prevent brute-force."""
    rate = '30/minute'


class VoteSubmitThrottle(AnonRateThrottle):
    """Limits vote submission attempts."""
    rate = '10/minute'


class ElectionViewSet(viewsets.ModelViewSet):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def results(self, request, pk=None):
        election = self.get_object()
        positions = Position.objects.filter(election=election)

        data = {
            'election': ElectionSerializer(election).data,
            'positions': []
        }

        for pos in positions:
            candidates = Candidate.objects.filter(position=pos).annotate(
                vote_count=Count('votes')
            ).order_by('-vote_count')

            pos_data = PositionSerializer(pos).data
            pos_data['candidates'] = []

            for cand in candidates:
                cand_data = CandidateSerializer(cand).data
                cand_data['vote_count'] = cand.vote_count
                pos_data['candidates'].append(cand_data)

            data['positions'].append(pos_data)

        return Response(data)

class PositionViewSet(viewsets.ModelViewSet):
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Supports server-side filtering via ?election=<id> query param."""
        queryset = Position.objects.all()
        election_id = self.request.query_params.get('election')
        if election_id:
            queryset = queryset.filter(election_id=election_id)
        return queryset

class PartylistViewSet(viewsets.ModelViewSet):
    queryset = Partylist.objects.all()
    serializer_class = PartylistSerializer
    permission_classes = [IsAuthenticated]

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]

class VoterViewSet(viewsets.ModelViewSet):
    queryset = Voter.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Use safe serializer (no token) by default; full serializer only for print_cards."""
        if self.action == 'print_cards':
            return VoterSerializer
        return VoterListSerializer

    @action(detail=False, methods=['GET'], url_path='print-cards')
    def print_cards(self, request):
        """Returns all voters WITH their voting tokens for printable cards."""
        voters = self.get_queryset()
        serializer = VoterSerializer(voters, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], url_path='import')
    def import_voters(self, request):
        file_obj = request.FILES.get('file', None)
        if not file_obj:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Assuming CSV with columns: student_id, name, email
            decoded_file = file_obj.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            created_count = 0
            for row in reader:
                _, created = Voter.objects.get_or_create(
                    student_id=row['student_id'],
                    defaults={
                        'name': row['name'],
                        'email': row['email']
                    }
                )
                if created:
                    created_count += 1

            return Response({'success': f'{created_count} voters imported successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'], url_path='revoke_token')
    def revoke_token(self, request, pk=None):
        voter = self.get_object()
        voter.regenerate_token()
        return Response({'success': 'Token regenerated successfully', 'new_token': voter.unique_voting_token}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['DELETE'], url_path='clear_all')
    def clear_all(self, request):
        count = Voter.objects.count()
        if count == 0:
            return Response({'message': 'No voters to remove.'}, status=status.HTTP_200_OK)
        Voter.objects.all().delete()
        return Response({'success': f'{count} voter(s) removed successfully.'}, status=status.HTTP_200_OK)

class VoteRecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VoteRecord.objects.all()
    serializer_class = VoteRecordSerializer
    permission_classes = [IsAuthenticated]

class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()

        # Turnout progression (votes per hour for the last 24 hours)
        turnout_data = []
        try:
            last_24h = now - timezone.timedelta(hours=24)
            progression = VoteRecord.objects.filter(timestamp__gte=last_24h) \
                .annotate(hour=TruncHour('timestamp')) \
                .values('hour') \
                .annotate(count=Count('id')) \
                .order_by('hour')

            for p in progression:
                hour_val = p.get('hour')
                label = '??'
                if hour_val:
                    if hasattr(hour_val, 'strftime'):
                        label = hour_val.strftime('%I %p')
                    else:
                        label = str(hour_val)
                turnout_data.append({'label': label, 'value': p.get('count', 0)})
        except Exception as e:
            print(f"Error calculating turnout progression: {e}")
            turnout_data = []

        stats = {
            'active_elections': Election.objects.filter(
                ~Q(status='DRAFT'),
                start_date__lte=now,
                end_date__gte=now
            ).count(),
            'total_candidates': Candidate.objects.count(),
            'total_voters': Voter.objects.count(),
            'total_votes': VoteRecord.objects.count(),
            'turnout_progression': turnout_data
        }
        return Response(stats)

class VoterLoginView(APIView):
    permission_classes = []  # Publicly accessible for login
    throttle_classes = [VoterLoginThrottle]

    def post(self, request):
        student_id = request.data.get('student_id')
        token = request.data.get('token')

        if not student_id or not token:
            return Response({'error': 'Student ID and Token are required'}, status=status.HTTP_400_BAD_REQUEST)

        now = timezone.now()
        active_elections_exist = Election.objects.filter(
            ~Q(status='DRAFT'),
            start_date__lte=now,
            end_date__gte=now
        ).exists()

        if not active_elections_exist:
            return Response({'error': 'There are no active elections at this time.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            with transaction.atomic():
                voter = Voter.objects.select_for_update().get(student_id=student_id, unique_voting_token=token)
                if voter.has_voted:
                    return Response({'error': 'You already casted a vote'}, status=status.HTTP_403_FORBIDDEN)
                
                if voter.is_active_session and voter.session_started_at:
                    if (now - voter.session_started_at).total_seconds() < 300: # 5 minutes
                        return Response({'error': 'A voting session is already active on another device'}, status=status.HTTP_403_FORBIDDEN)
                
                voter.is_active_session = True
                voter.session_started_at = now
                voter.save()
                
            serializer = VoterSerializer(voter)
            
            encoded_jwt = jwt.encode({
                'voter_id': voter.id, 
                'student_id': voter.student_id,
                'exp': now + timezone.timedelta(minutes=5)
            }, settings.SECRET_KEY, algorithm='HS256')
            
            data = serializer.data
            data['access_token'] = encoded_jwt
            
            return Response(data)
        except Voter.DoesNotExist:
            return Response({'error': 'Invalid Student ID or Token'}, status=status.HTTP_401_UNAUTHORIZED)

class ActiveElectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ElectionSerializer
    permission_classes = []
    authentication_classes = []

    def get_queryset(self):
        now = timezone.now()
        return Election.objects.filter(
            ~Q(status__in=['DRAFT', 'COMPLETED']),
            start_date__lte=now,
            end_date__gte=now
        )

    @action(detail=True, methods=['GET'])
    def ballot(self, request, pk=None):
        election = self.get_object()
        positions = Position.objects.filter(election=election)

        data = []
        for pos in positions:
            candidates = Candidate.objects.filter(position=pos)
            pos_data = PositionSerializer(pos).data
            pos_data['candidates'] = CandidateSerializer(candidates, many=True).data
            data.append(pos_data)

        return Response(data)

class BallotSubmissionView(APIView):
    permission_classes = []  # We manually check the custom JWT
    authentication_classes = []
    throttle_classes = [VoteSubmitThrottle]

    def post(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response({'error': 'Authentication required. Please log in again.'}, status=status.HTTP_401_UNAUTHORIZED)
            
        jwt_token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
            voter_id = payload['voter_id']
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Voting session expired. Please log in again.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid session token.'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = SubmitVoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        election_id = serializer.validated_data['election_id']
        selections = serializer.validated_data['selections']

        try:
            now = timezone.now()
            
            try:
                election = Election.objects.get(id=election_id)
            except Election.DoesNotExist:
                return Response({'error': 'Election not found'}, status=status.HTTP_404_NOT_FOUND)

            if election.status == 'DRAFT':
                return Response({'error': 'This election is not yet published (Draft mode).'}, status=status.HTTP_400_BAD_REQUEST)
            if election.status == 'COMPLETED' or now > election.end_date:
                return Response({'error': 'Voting for this election has already ended.'}, status=status.HTTP_400_BAD_REQUEST)
            if now < election.start_date:
                return Response({'error': f'Voting has not started yet. Starts at {election.start_date.strftime("%Y-%m-%d %H:%M")}'}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                voter = Voter.objects.select_for_update().get(id=voter_id)
                if voter.has_voted:
                    return Response({'error': 'Vote already cast'}, status=status.HTTP_403_FORBIDDEN)
                    
                records = []
                for candidate_id in selections:
                    candidate = Candidate.objects.get(id=candidate_id)
                    records.append(VoteRecord(
                        election=election,
                        position=candidate.position,
                        candidate=candidate
                    ))
                VoteRecord.objects.bulk_create(records)

                voter.has_voted = True
                voter.is_active_session = False
                voter.save()

            return Response({'success': 'Vote cast successfully'}, status=status.HTTP_201_CREATED)
        except (Voter.DoesNotExist, Candidate.DoesNotExist) as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

