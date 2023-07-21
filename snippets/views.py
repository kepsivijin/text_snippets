from rest_framework.permissions import IsAuthenticated
from .models import Snippet, Tag
from rest_framework import generics, viewsets
from .serializers import SnippetSerializer, TagSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Snippet
from .serializers import SnippetCreateSerializer



class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = SnippetCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Save the snippet data to the database
            snippet = serializer.save()
            return Response({
                "message": "Snippet created successfully.",
                "data": serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, id=None):
        if id:
            queryset = Snippet.objects.filter(id=id)
        else:
            queryset = Snippet.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        # Create hyperlinks to respective detail APIs for each snippet
        data = []
        for snippet in serializer.data:
            # snippet['detail_url'] = reverse('snippets', args=[snippet['id']], request=request)
            snippet['detail_url'] = reverse('snippets_call-detail' ,kwargs={'pk': snippet['id']}, request=request)
            data.append(snippet)

        total_count = Snippet.objects.count()
        return Response({
            "total Count":total_count,
            "data":data
        })

    def retrieve(self, request, pk=None):
        queryset = Snippet.objects.filter(id=pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TagDetailViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Tag.objects.filter(id=pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
