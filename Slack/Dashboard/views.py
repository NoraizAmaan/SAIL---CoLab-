from django.shortcuts import render, HttpResponse

from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from Dashboard.serializers import GroupSerializer, UserSerializer

# Create your views here.
def DashboardHome(request):
    return render(request, 'dashboardhome.html')
    #return HttpResponse('This is DashboardHome. We will keep all the posts here')

def DashboardPost(request, slug):
    return render(request, 'dashboardPost.html')
    #return HttpResponse(f'This is DashboardPost: {slug}')


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]