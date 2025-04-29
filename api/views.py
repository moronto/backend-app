from django.shortcuts import render, get_object_or_404
from rest_framework import status
from api.serializers import *
from inventaire.models import *
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
import json
from django.http import JsonResponse



#views Stock management
class StockData(ModelViewSet):
    queryset=Stock.objects.all().order_by('-created_at')
    serializer_class=StockSerializer

@api_view(['GET','PUT'])
def detailStock(request, ref):
    data=[]
    try:
        mat = get_object_or_404(Stock, refMateriel=ref)
        serializer = StockSerializer(mat)
        data.append(serializer.data)
        
        if serializer.data['categorie']=="GROUPE ELECTROGENE":
            GE=get_object_or_404(GroupeElectrogene, refMateriel=ref)
            serializerGE=GroupeElectrogeneSerializer(GE)
            data.append(serializerGE.data)
        elif serializer.data['categorie']=="MODULAIRE":
            MOD=get_object_or_404(Modulaire,refMateriel=ref)
            serializerMOD=ModulaireSerializer(MOD)
            data.append(serializerMOD.data)
        elif serializer.data['categorie']=="CABINES AUTONOMES":
            CAB=get_object_or_404(CabinesAutonome,refMateriel=ref)
            serializerCAB=CabinesAutonomeSerializer(CAB)
            data.append(serializerCAB.data)
                
        
        return Response({
            'status': 'success',
            'data': data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
@api_view(['POST','GET'])
def addStock(request):
    data={}
    
    if request.method == 'POST':

        data=request.data
        st=Stock.objects.get_or_create(
        refMateriel=data.get('refMateriel'),
        designation=data.get('designation'),
        situation="DISPONIBLE",
        lieu=data.get('lieu'),
        categorie=data.get('categorie'),
        )
        

        print(data.get('dimension'))

        if data.get('categorie')=='GROUPE ELECTROGENE':
            print('hayi')
            GE=GroupeElectrogene.objects.get_or_create(
                puissance=data.get('puissance'),
                marque=data.get('marque'),
                dimension=data.get('dimension'),
                refMateriel=st[0],
            )
            
        elif  data.get('categorie')=='MODULAIRE':
            MOD=Modulaire.objects.get_or_create(
                gamme=data.get('gamme'),
                dimension=data.get('dimension'),
                refMateriel=st[0],
            )
            
        elif  data.get('categorie')=='CABINES AUTONOMES':
            CAB=CabinesAutonome.objects.get_or_create(
                gamme=data.get('gamme'),
                dimension=data.get('dimension'),
                color=data.get('color'),
                refMateriel=st[0],
            )
             

    return Response(data) 

@api_view(['PUT','GET'])
def updateStock(request,ref):
    data={}
    updatedData=request.data
    if request.method == 'PUT':

        data=request.data
        st=Stock.objects.get(refMateriel=ref)
        
        st.refMateriel=data.get('refMateriel')
        st.designation=data.get('designation')
        st.situation=data.get('situation')
        st.client=data.get('client')
        st.lieu=data.get('lieu')
        st.categorie=data.get('categorie')

        st.save()
        
        
   

        if data.get('categorie')=='GROUPE ELECTROGENE':
            
            GE=GroupeElectrogene.objects.get(refMateriel=ref)
            GE.puissance=data.get('puissance')
            GE.marque=data.get('marque')
            GE.dimension=data.get('dimension')
            GE.refMateriel=st

            GE.save()
            
            
        elif  data.get('categorie')=='MODULAIRE':
            MOD=Modulaire.objects.get(refMateriel=ref)
            MOD.gamme=data.get('gamme')
            MOD.dimension=data.get('dimension')
            MOD.refMateriel=st
            MOD.save()
            
        elif  data.get('categorie')=='CABINES AUTONOMES':
            CAB=CabinesAutonome.objects.get(refMateriel=ref)
            CAB.gamme=data.get('gamme')
            CAB.dimension=data.get('dimension')
            CAB.color=data.get('color')
            CAB.refMateriel=st

            CAB.save()
             

    return Response({'msg':"Modification effectuer avec success",
                     'status':status.HTTP_200_OK}) 

@api_view(['DELETE'])
def deleteStock(request,ref):
    try:
       stock=Stock.objects.get(refMateriel=ref)
    except Stock.DoesNotExist :
        return Response(
            {"erreur":"ce materiel n'existe pas"},
            status=status.HTTP_404_NOT_FOUND
        )  
    stock.delete()
    
    return Response(
        status=status.HTTP_200_OK
    )
    
# views Movements management
class movements(ModelViewSet):
    queryset=Movement.objects.all() 
    serializer_class=MovementSerializer

@api_view(['GET'])
def getMovement(request,id):
    move=Movement.objects.get(id=id) 
    serializer=MovementSerializer(move)
    return Response(serializer.data)   

