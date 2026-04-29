from rest_framework import serializers
from .models import Election, Position, Partylist, Candidate, Voter, VoteRecord

class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = ['id', 'title', 'start_date', 'end_date', 'status', 'calculated_status']

class PositionSerializer(serializers.ModelSerializer):
    election_title = serializers.CharField(source='election.title', read_only=True)
    
    class Meta:
        model = Position
        fields = '__all__'

class PartylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partylist
        fields = '__all__'

class CandidateSerializer(serializers.ModelSerializer):
    position_name = serializers.CharField(source='position.name', read_only=True)
    partylist_name = serializers.CharField(source='partylist.name', read_only=True)
    
    class Meta:
        model = Candidate
        fields = '__all__'

class VoterListSerializer(serializers.ModelSerializer):
    """Safe serializer for admin table views — excludes the sensitive voting token."""
    class Meta:
        model = Voter
        fields = ['id', 'student_id', 'name', 'email', 'has_voted']

class VoterSerializer(serializers.ModelSerializer):
    """Full serializer with token — used only for voter login and print-cards endpoint."""
    class Meta:
        model = Voter
        fields = ['id', 'student_id', 'name', 'email', 'has_voted', 'unique_voting_token']

class VoteRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteRecord
        fields = '__all__'

class SubmitVoteSerializer(serializers.Serializer):
    election_id = serializers.IntegerField()
    selections = serializers.ListField(child=serializers.IntegerField())
