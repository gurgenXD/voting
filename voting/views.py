from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from voting.models import Voting, PersonVotes
from voting.tasks import create_xlsx, send_email


class ActiveVotingView(View):
    def get(self, request):
        votings = Voting.objects.all()
        return render(request, 'active_voting.html', {'votings': votings})


class VotingPageView(View):
    def get(self, request, voting_id):
        is_voted = False
        if voting_id in request.session.get('is_voted_list'):
            is_voted = True

        voting = get_object_or_404(Voting, id=voting_id)
        return render(request, 'voting_page.html', {'voting': voting, 'is_voted': is_voted})

    def post(self, request, voting_id):
        is_voted_list = request.session.get('is_voted_list')

        if voting_id not in is_voted_list:
            person_vote_id = request.POST.get('person_vote_id')
            person_vote = PersonVotes.objects.get(id=int(person_vote_id))
            person_vote.votes += 1
            person_vote.save()
            is_voted_list.append(voting_id)
            request.session.modified = True

        return redirect(request.path)


class NotActiveVotingView(View):
    def get(self, request):
        votings = Voting.objects.all()
        return render(request, 'not_active_voting.html', {'votings': votings})

class CreateXlsxView(View):
    def get(self, request, voting_id):
        voting = Voting.objects.get(id=voting_id)
        voting.xlsx_status = 2
        voting.save()

        create_xlsx.delay(voting_id)
        if request.user.email:
            send_email.delay(request.user.email)
        return redirect('/admin/voting/voting/')
