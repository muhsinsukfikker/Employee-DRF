from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import authentication,permissions
from api.models import Employees,Tasks
from api.serializers import EmpSerializer,TaskSerializer
# Create your views here.


class EmployeeViewSetView(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        qs=Employees.objects.all()
        serializer=EmpSerializer(qs,many=True)
        return Response(data=serializer.data)
    

    def create(self, request, *args, **kwargs):
        serializer=EmpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        


    def retrieve(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        qs=Employees.objects.get(id=id)
        serializer=EmpSerializer(qs)
        return Response(data=serializer.data)
    


    def update(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        mob_obj=Employees.objects.get(id=id)
        serializer=EmpSerializer(data=request.data,instance=mob_obj)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

    def destroy(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        Employees.objects.get(id=id).delete()

        return Response(data={'message': 'Deleted'})


class EmployeeModelViewSetViewSet(viewsets.ModelViewSet):
    
    permission_classes=[permissions.IsAdminUser]
    authentication_classes=[authentication.TokenAuthentication]

    serializer_class = EmpSerializer
    model=Employees
    queryset=Employees.objects.all()

    def list(self, request, *args, **kwargs):
        qs=Employees.objects.all()
        if 'department' in request.query_params:
            value=request.query_params.get('department')
            qs=qs.filter(department=value)

        serializer=EmpSerializer(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=['get'],detail=False)
    def dept(self, request, *args, **kwargs):
        qs=Employees.objects.all().values_list('department', flat=True).distinct()
        return Response(data=qs)
    

    #assign task to employee
    #localhost:8000/api/v1/emp/{id}/add_task/
    @action(methods=['post'],detail=True)
    def add_task(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        emp_obj=Employees.objects.get(id=id)
        serializer=TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=emp_obj)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    #specific emp tasks
    #localhost:8000/api/v1/emp/{id}/tasks/
    @action(methods=['get'],detail=True)
    def tasks(self, request,*args,**kwargs):
            id=kwargs.get('pk')
            qs=Tasks.objects.filter(employee__id=id)
            serializer=TaskSerializer(qs,many=True)
            return Response(data=serializer.data)
           

#localhost:8000/api/v1/task/{id}/
#methods:put
class TasksView(viewsets.ViewSet):
        
        permission_classes=[permissions.IsAuthenticated]
        authentication_classes=[authentication.TokenAuthentication]

        def update(self,request,*args,**kwargs):
            id=kwargs.get('pk')
            task_obj=Tasks.objects.get(id=id)
            serializer=TaskSerializer(data=request.data,instance=task_obj)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)
            

        def retrieve(self,request,*args,**kwargs):
            id=kwargs.get('pk')
            qs=Tasks.objects.get(id=id)
            serializer=TaskSerializer(qs)
            return Response(data=serializer.data)
        
        def destroy(self,request,*args,**kwargs):
            id=kwargs.get('pk') 
            Tasks.objects.get(id=id).delete()
            return Response(data={'status':'deleted'})



