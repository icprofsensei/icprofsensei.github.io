from django.shortcuts import get_object_or_404
from register.models import UserProfile  # Adjust to your app name
from polls.models import Question

def organisation(request):
    if request.user.is_authenticated:
        try:
            # Get the user's profile
            user_profile = UserProfile.objects.get(user=request.user)
            organisation = user_profile.organisation
            
            # Get all questions related to the user's organisation
            questions = Question.objects.filter(organisation=organisation)
            
            # Return both organisation and questions
            return {
                'username': user_profile.user,  # Get the user from the profile
                'organisation': organisation,
                'orgquestions': questions
            }
        except UserProfile.DoesNotExist:
            # Handle the case where UserProfile does not exist
            return {
                'username': request.user,  # Still return the user
                'organisation': None,
                'orgquestions': None
            }
    
    # Return None for both if the user is not authenticated
    return {
        'username': None,
        'organisation': None,
        'orgquestions': None
    }