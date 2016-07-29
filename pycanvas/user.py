from canvas_object import CanvasObject
from paginated_list import PaginatedList
from upload import Uploader
from util import combine_kwargs, obj_or_id


class User(CanvasObject):

    def __str__(self):
        return "%s" % (self.name)

    def get_profile(self, **kwargs):
        """
        Retrieve this user's profile.

        :calls: `GET /api/v1/user/:id \
        <https://canvas.instructure.com/doc/api/users.html#method.profile.settings>`_

        :rtype: dict
        """
        response = self._requester.request(
            'GET',
            'users/%s/profile' % (self.id)
        )
        return response.json()

    def get_page_views(self, **kwargs):
        """
        Retrieve this user's page views.

        :calls: `GET /api/v1/users/:user_id/page_views \
        <https://canvas.instructure.com/doc/api/users.html#method.page_views.index>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.course.PageView`
        """
        from page_view import PageView

        return PaginatedList(
            PageView,
            self._requester,
            'GET',
            'users/%s/page_views' % (self.id),
            **combine_kwargs(**kwargs)
        )

    def get_courses(self, **kwargs):
        """
        Retrieve all courses this user is enrolled in.

        :calls: `GET /api/v1/users/:user_id/courses \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.user_index>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.course.Course`
        """
        from course import Course

        return PaginatedList(
            Course,
            self._requester,
            'GET',
            'users/%s/courses' % (self.id),
            **combine_kwargs(**kwargs)
        )

    def get_missing_submissions(self):
        """
        Retrieve all past-due assignments for which the student does not
        have a submission.

        :calls: `GET /api/v1/users/:user_id/missing_submissions \
        <https://canvas.instructure.com/doc/api/users.html#method.users.missing_submissions>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.assignment.Assignment`
        """
        from assignment import Assignment

        return PaginatedList(
            Assignment,
            self._requester,
            'GET',
            'users/%s/missing_submissions' % (self.id)
        )

    def update_settings(self, **kwargs):
        """
        Update this user's settings.

        :calls: `PUT /api/v1/users/:id/settings \
        <https://canvas.instructure.com/doc/api/users.html#method.users.settings>`_

        :rtype: dict
        """
        response = self._requester.request(
            'PUT',
            'users/%s/settings' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return response.json()

    def get_color(self, asset_string):
        """
        Return the custom colors that have been saved by this user for a given context.

        The `asset_string` parameter should be in the format 'context_id', for example 'course_42'.

        :calls: `GET /api/v1/users/:id/colors/:asset_string \
        <https://canvas.instructure.com/doc/api/users.html#method.users.get_custom_color>`_

        :param asset_string: The asset to retrieve the color from.
        :type asset_string: str
        :rtype: dict
        """
        response = self._requester.request(
            'GET',
            'users/%s/colors/%s' % (self.id, asset_string)
        )
        return response.json()

    def get_colors(self):
        """
        Return all custom colors that have been saved by this user.

        :calls: `GET /api/v1/users/:id/colors \
        <https://canvas.instructure.com/doc/api/users.html#method.users.get_custom_colors>`_

        :rtype: dict
        """
        response = self._requester.request(
            'GET',
            'users/%s/colors' % (self.id)
        )
        return response.json()

    def update_color(self, asset_string, hexcode):
        """
        Update a custom color for this user for a given context.

        This allows colors for the calendar and elsewhere to be customized on a user basis.

        The `asset_string` parameter should be in the format 'context_id', for example 'course_42'.
        The `hexcode` parameter need not include the '#'.

        :calls: `PUT /api/v1/users/:id/colors/:asset_string \
        <https://canvas.instructure.com/doc/api/users.html#method.users.set_custom_color>`_

        :param asset_string: The asset to modify the color for.
        :type asset_string: str
        :param hexcode: The hexcode of the color to use.
        :type hexcode: str
        :rtype: dict
        """
        response = self._requester.request(
            'PUT',
            'users/%s/colors/%s' % (self.id, asset_string),
            hexcode=hexcode
        )
        return response.json()

    def edit(self, **kwargs):
        """
        Modify this user's information.

        :calls: `PUT /api/v1/users/:id \
        <https://canvas.instructure.com/doc/api/users.html#method.users.update>`_

        :rtype: :class:`pycanvas.user.User`
        """
        response = self._requester.request(
            'PUT',
            'users/%s' % (self.id),
            **combine_kwargs(**kwargs)
        )
        super(User, self).set_attributes(response.json())
        return self

    def merge_into(self, destination_user):
        """
        Merge this user into another user.

        :calls: `PUT /api/v1/users/:id/merge_into/:destination_user_id \
        <https://canvas.instructure.com/doc/api/users.html#method.users.merge_into>`_

        :param destination_user: The user to merge into.
        :type destination_user: :class:`pycanvas.user.User`
        :rtype: :class:`pycanvas.user.User`
        """
        dest_user_id = obj_or_id(destination_user, 'destination_user', (User, ))

        response = self._requester.request(
            'PUT',
            'users/%s/merge_into/%s' % (self.id, dest_user_id),
        )
        super(User, self).set_attributes(response.json())
        return self

    def get_avatars(self):
        """
        Retrieve the possible user avatar options that can be set with the user update endpoint.

        :calls: `GET /api/v1/users/:user_id/avatars \
        <https://canvas.instructure.com/doc/api/users.html#method.profile.profile_pics>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.avatar.Avatar`
        """
        from avatar import Avatar

        return PaginatedList(
            Avatar,
            self._requester,
            'GET',
            'users/%s/avatars' % (self.id)
        )

    def get_assignments(self, course_id, **kwargs):
        """
        Return the list of assignments for this user if the current
        user (the API key owner) has rights to view. See List assignments for valid arguments.

        :calls: `GET /api/v1/users/:user_id/courses/:course_id/assignments \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.user_index>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.assignment.Assignment`
        """
        from assignment import Assignment

        return PaginatedList(
            Assignment,
            self._requester,
            'GET',
            'users/%s/courses/%s/assignments' % (self.id, course_id),
            **combine_kwargs(**kwargs)
        )

    def get_enrollments(self, **kwargs):
        """
        List all of the enrollments for this user.

        :calls: `GET /api/v1/users/:user_id/enrollments \
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.enrollment.Enrollment`
        """
        from enrollment import Enrollment

        return PaginatedList(
            Enrollment,
            self._requester,
            'GET',
            'users/%s/enrollments' % (self.id),
            **combine_kwargs(**kwargs)
        )

    def upload(self, file, **kwargs):
        """
        Upload a file for a user.

        NOTE: You *must* have authenticated with this user's API key to
        upload on their behalf no matter what permissions the issuer of the
        request has.

        :calls: `POST /api/v1/users/:user_id/files \
        <https://canvas.instructure.com/doc/api/users.html#method.users.create_file>`_

        :param path: The path of the file to upload.
        :type path: str
        :param file: The file or path of the file to upload.
        :type file: file or str
        :returns: True if the file uploaded successfully, False otherwise, \
                    and the JSON response from the API.
        :rtype: tuple
        """
        return Uploader(
            self._requester,
            'users/%s/files' % (self.id),
            file,
            **kwargs
        ).start()
