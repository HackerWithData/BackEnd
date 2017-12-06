# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from allauth.socialaccount.views import SignupView, ConnectionsView
from allauth.socialaccount import helpers
from ..user_helpers import (retrieve_professional_info,
                           get_professional_corresponding_object_by_type_and_lic,
                           get_professional_user,
                           generate_random_hoome_id)


class Signup(SignupView):
    def form_valid(self, form):
        # By assigning the User to a property on the view, we allow subclasses
        # of SignupView to access the newly created User instance
        # print(self.request.POST)
        # self.request.POST['hoome_id'] = generate_random_hoome_id()
        # TODO: there is a better way to add hoome_id when using adapter
        form.save(self.request)
        self.user.hoome_id = generate_random_hoome_id()
        self.user.save()
        return helpers.complete_social_signup(self.request,
                                              self.sociallogin)

