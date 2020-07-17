def context_info(request):
    is_voted_list = request.session.get('is_voted_list')

    if not is_voted_list:
        request.session['is_voted_list'] = []

    return {}