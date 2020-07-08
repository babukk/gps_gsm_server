
from datetime import datetime, timedelta
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.schemas import SchemaGenerator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Transport, TransportData
from .serializers import TransportSerializer, TransportDataSerializer, TrackDataSerializer


# @api_view()
# @permission_classes((AllowAny, ))
# @renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
# def schema_view(request):
#     generator = SchemaGenerator(title='Rest Swagger')

#     return Response(generator.get_schema(request=request))


class TransportView(APIView):
    """ Возвращает массив трекеров """

    def get(self, request):
        transports = Transport.objects.all()

        serializer = TransportSerializer(transports, many=True)

        return Response({"transports": serializer.data})


class TransportDataCurrentPosView(APIView):
    """ Возвращает текущую (последнюю) позицию трекера """

    def get(self, request, id):

        tranport_data = TransportData.objects.filter(id_user_transport=id).order_by('-id')[:1]
        serializer = TransportDataSerializer(tranport_data, many=True)

        return Response({"tracker_data": serializer.data})


class TrackDataView(APIView):
    """ Возвращает данные трека (массив точек) """

    def get(self, request, id):
        """
        date_from -- дата-время начала
        date_to -- дата-время конца
        """
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        # track_data = [{'date_from': date_from, 'date_to': date_to}]
        track_data = TransportData.objects.filter(id_user_transport=id).filter(when_added__gte=datetime.now() - timedelta(days=30)).filter(speed__gt=0).order_by('id')[:300]

        serializer = TrackDataSerializer(track_data, many=True)
        # return Response({"track_data": track_data})

        return Response({"track_data": serializer.data})
