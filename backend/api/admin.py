from django.contrib import admin
from .models import Election, Position, Partylist, Candidate, Voter, VoteRecord


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'start_date', 'end_date']
    list_filter = ['status']
    search_fields = ['title']


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['name', 'election', 'max_votes_allowed', 'hierarchy_order']
    list_filter = ['election']
    ordering = ['election', 'hierarchy_order']


@admin.register(Partylist)
class PartylistAdmin(admin.ModelAdmin):
    list_display = ['name', 'election']
    list_filter = ['election']


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'partylist', 'course_and_year']
    list_filter = ['position__election', 'partylist']
    search_fields = ['name']


@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'name', 'email', 'has_voted']
    list_filter = ['has_voted']
    search_fields = ['student_id', 'name', 'email']


@admin.register(VoteRecord)
class VoteRecordAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'position', 'election', 'timestamp']
    list_filter = ['election', 'position']
    ordering = ['-timestamp']
