from django.http import QueryDict
from django.shortcuts import render

from rest_framework.generics import (ListCreateAPIView,
                                     CreateAPIView,
                                     ListAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from . import models as agent_models
from . import serializers as agent_serializers

from apps.mixins.functions import generate_agent_branch_code




#====================== AGENT ====================================
# class AgentCreateView(CreateAPIView):
#     queryset = agent_models.Agent.objects.all()
#     serializer_class = agent_serializers.AgentCreateSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly,]


class AgentListCreateView(ListCreateAPIView):
    queryset = agent_models.Agent.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def get_serializer_class(self):
        if self.request is not None:
            if self.request.method == "GET":
                return agent_serializers.AgentSerializer
            else:
                return agent_serializers.AgentCreateSerializer
        else:
            return agent_serializers.AgentCreateSerializer


class AgentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = agent_models.Agent.objects.all()
    serializer_class = agent_serializers.AgentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]



#====================== AGENT BRANCH====================================
class AgentBranchListCreateView(ListCreateAPIView):
    queryset = agent_models.AgentBranch.objects.all()
    serializer_class = agent_serializers.AgentBranchSerializer

    def get(self, request, pk):
        try:
            agent = agent_models.Agent.objects.get(pk=pk)
        except agent_models.Agent.DoesNotExist:
            return Response({"detail": f"No Agent found with id {pk}!"}, status=status.HTTP_404_NOT_FOUND )

        agent_branches = agent.branches.all()
        return Response({"detail": self.serializer_class(agent_branches, many=True).data}, 
                        status=status.HTTP_200_OK)
   
class AgentBranchRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = agent_models.AgentBranch.objects.all()
    serializer_class = agent_serializers.AgentBranchSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]


#====================== AGENT ADMIN ====================================
class AgentAdminListCreateView(ListCreateAPIView):
    # queryset = agent_models.AgentAdmin.objects.all()
    serializer_class = agent_serializers.AgentAdminSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]


    def get_queryset(self):
        branch_id = self.kwargs["pk"]
        agent_admins = agent_models.AgentAdmin.objects.filter(agent_branch=branch_id)
        return agent_admins


class AgentAdminRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = agent_models.AgentAdmin.objects.all()
    serializer_class = agent_serializers.AgentAdminRetrieveUpdateDestroySerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def delete(self, request, pk):
        admins = agent_models.AgentAdmin.objects.all()
        if admins.get(pk=pk).is_superadmin:
            return Response({"detail": "Super admin user can not be deleted. Consider changing to non super user before deleting."},
                            status=status.HTTP_403_FORBIDDEN)
        elif not admins.get(pk=pk).is_superadmin and admins.count() == 1:
            return Response({"detail": "Operation cannot be completed. At least one admin is required!"},
                            status=status.HTTP_403_FORBIDDEN)
        
        agent_models.AgentAdmin.objects.get(pk=pk).delete()
        return Response({"detail": "Admin deleted!"},
                            status=status.HTTP_200_OK)
    
    
    