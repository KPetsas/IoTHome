class DevicesCache():
    """
    The Cache is a JSON object with three elements:
    1. Primary key: pk.
    2. user_id to primary key, octal converted to avoid user_id overlap.
    3. Octal converted value to list of user devices.

    Example of cache:

    {'pk': 2, '1': '0o1', '0o1': [{'name': 'Smart Socket', 'switch_state': False, 'device_ui_id': 'smart_socket', 'state': 'online', 'status': 'off'}]}
    """

    def init_app(self, app):
        """ Constructor initializations. """
        self._INITIAL_PRIMARY_KEY = 1  # decimal 1 to octal is 001 in ASCII table

        self._logger = app.logger
        self._cache = dict(pk=self._INITIAL_PRIMARY_KEY)

    @property
    def cache(self):
        """ Cache getter. """
        self._logger.debug("Get Cache.")
        return self._cache

    @cache.setter
    def cache(self, user_id_devices_list_tuple):
        """
        Cache setter.

        :param user_id_devices_list_tuple: The user id and a list of the user devices.
        """
        try:
            user_id, devices_list = user_id_devices_list_tuple
        except ValueError:
            raise ValueError("Input must be an iterable with two items: (user_id, devices_list)")
        else:
            self._logger.debug(
                "Set Cache for user with ID {} and user_devices_list: {}".format(user_id, devices_list))
            cache_pk = self._cache.get("pk")
            self._cache[str(user_id)] = oct(cache_pk)
            self._cache[oct(cache_pk)] = devices_list
            self._cache["pk"] = cache_pk + 1

    def get_user_cache(self, user_id):
        """
        Get the user related devices list from cache.

        :param (int) user_id: The current user id.
        :return: List of devices as objects.
        """
        return self._cache.get(self._cache.get(str(user_id)), list())

    def find_device_status(self, user_id, device_ui_id):
        """
        Find the status of the specified device.

        :param (int) user_id: The current user id.
        :param (str) device_ui_id: The unique device id used in UI.
        :return: Device status
        :rtype: str
        """
        for device_dict in self.get_user_cache(user_id):
            if device_dict.get('device_ui_id') == device_ui_id:
                return device_dict.get('status')

    def update_cache(self, user_id, device_ui_id, fields_dict):
        """
        Update the cache with the values specified in the fields_dict parameter.

        :param (int) user_id: The current user id.
        :param (str) device_ui_id: The unique device id used in UI.
        :param (dict) fields_dict: The fields to update in the retrieved device model.
        """
        for device_dict in self.get_user_cache(user_id):
            if device_dict.get('device_ui_id') == device_ui_id:
                device_dict.update(fields_dict)
                break

    def clear_cache(self):
        """ Clear and initialize the cache dict. """
        self._logger.debug("Clear Cache.")
        self._cache.clear()
        self._cache = dict(pk=self._INITIAL_PRIMARY_KEY)

    def clear_user_cache(self, user_id):
        """
        Remove user_id and the related cached devices.

        :param (int) user_id: The current user id.
        """
        if self.get_user_cache(user_id):
            self._cache.pop(self._cache.get(str(user_id)))
            self._cache.pop(str(user_id))
