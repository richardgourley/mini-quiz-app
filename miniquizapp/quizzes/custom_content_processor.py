# Returns session variables as a list (if session is active)

def latest_quiz_visited_info(request):
    latest_quiz_visited_info = {}
    if 'most_recent_quiz_title' in request.session:
        latest_quiz_visited_info['title'] = request.session['most_recent_quiz_title']
        latest_quiz_visited_info['url'] = request.session['most_recent_quiz_url']
        return {
            'latest_quiz_visited_info': latest_quiz_visited_info
        }
    else:
        return {
            'latest_quiz_visited_info': None
        }

