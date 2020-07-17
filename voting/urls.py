from django.urls import path
from voting.views import ActiveVotingView, VotingPageView, NotActiveVotingView


urlpatterns = [
    path('', ActiveVotingView.as_view(), name='active_voting'),
    path('not-active', NotActiveVotingView.as_view(), name='not_active_voting'),
    path('votings/<int:voting_id>', VotingPageView.as_view(), name='voting_page'),
]