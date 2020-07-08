
import os
import sys

try:
    sys.path.append(os.environ['DJANGO_PROJECT_PATH'])
    # sys.path.append(os.environ['DJANGO_PROJECT_PATH'] + '/gpsserver')
except:
    pass

os.environ['DJANGO_SETTINGS_MODULE'] = 'gpsserver.settings'

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.contrib.gis.geos import Point
from django.utils import timezone

application = get_wsgi_application()

from gpsserver.models import Transport as DjTransport, TransportData as DjTransportData
from users.models import CustomUser as DjCustomUser


class TransportCustom(object):
    pass


class TransportWialon(object):

    def check_login(self, _imei):
        try:
            device = DjTransport.objects.get(imei__exact=_imei)
            return device.id_user_transport, None
        except Exception as e:
            return None, str(e)


class TransportDataCustom(object):

    def save_data(self, user_id, dt, tm, lat, lon, course, speed, altitude, sats, flags1):
        if speed == "empty": speed = None
        if course == "empty": course = None
        if altitude == "empty": altitude = None
        if sats == "empty": sats = None
        if flags1 == "empty": flags1 = None

        try:
            ptn = Point(float(lon), float(lat))
            new_data = DjTransportData(
                user_id=user_id,
                point=ptn,
                altitude=altitude,
                speed=speed,
                satellite=sats,
                flags1=flags1,
            )
            new_data.save()
            # print('---- new_data.id = ', new_data.id)
        except Exception as e:
            return False, str(e)

        return True, None


class TransportDataWialon(object):

    def save_data(self, transport_id, dt, lat, lon, course, speed, altitude, sats):
        if lat is None or lon is None:
            return False, "Empty coordinate(s)."

        dt = timezone.make_aware(dt, timezone.get_current_timezone())


        if speed == "NA": speed = None
        if course == "NA": course = None
        if altitude == "NA": altitude = None
        if sats == "NA": sats = None

        # print("TransportDataWialon::save_data: lat = ", lat, "; lon = ", lon, "; dt = ", dt)

        try:
            ptn = Point(float(lon), float(lat))
            new_data = DjTransportData(
                id_user_transport_id=transport_id,
                point=ptn,
                when_added=dt,
                altitude=altitude,
                speed=speed,
                satellite=sats
            )
            # print("TransportDataWialon::save_data: new_data = ", new_data)
            new_data.save()
        except Exception as e:
            return False, str(e)

        return True, None


class CustomUser(object):

    def check_login(self, _username, _password):
        try:
            user = DjCustomUser.objects.get(username__exact=_username, password__exact=_password)
            return user.id_user, None
        except Exception as e:
            return None, str(e)
