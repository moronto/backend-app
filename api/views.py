from django.shortcuts import render, get_object_or_404
from django.db.models import Count
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

#display chart
@api_view(['GET'])
def statistiquesMovement(request):
    movement=Movement.objects.all()
    serializer=MovementSerializer(movement, many=True)

    return Response(serializer.data)
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
        st.ville=data.get('ville')
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
    queryset=Movement.objects.all().order_by('-dateMovement')
    serializer_class=MovementSerializer

@api_view(['GET'])
def getMovement(request,id):
    move=Movement.objects.get(id=id) 
    serializer=MovementSerializer(move)
    return Response(serializer.data)   


@api_view(['POST','GET'])
def addSortie(request):
    if request.method=='POST':
        move=MovementSerializer(data=request.data)
        if move.is_valid():
            move.save()
            m=request.data.get('refMateriel')
            st=Stock.objects.get(refMateriel=m)
            st.situation='LOUER'
            st.lieu=request.data.get('lieu')
            st.ville=request.data.get('ville')
            st.save()
            return Response({'msg':f'Vous avez ajouter le {request.POST.get("typeMovement")} de {request.POST.get("refMateriel")}'})   
        else:
            return Response({'msg':f'Probleme est servenu lors d enrigistrement de mouvement'})   


@api_view(['GET','POST'])
def infoMateriel(request,ref):
    mat=Stock.objects.get(refMateriel=ref)
    ser=StockSerializer(mat)
    return Response({'data':ser.data}) 
       
        
@api_view(['POST'])
def retirerMateriel(request):
    if request.method=='POST':
        try:
            serializer=MovementSerializer(data=request.data)
            if serializer.is_valid():
                mat=serializer.save()
                m=request.data.get('refMateriel')
                print(m)
                st=Stock.objects.get(refMateriel=m)
                st.situation='DISPONIBLE'
                st.lieu= f"DEPOT   {request.data.get('lieu')}"
                st.ville=request.data.get('lieu')
                st.save()
            else:
              print(serializer.errors)    
          

        except Exception as e:

           return Response({'error':str(e),})     
    return Response({'msg': f'Vous avez retirer {request.data.get("refMateriel")} avec succes'})

@api_view(['DELETE'])  
def deleteMovement(request,id):
    if request.method=='DELETE':
        try:
           move=Movement.objects.get(id=id) 
           move.delete()
        
           return Response({"msg":f'Vous avez suprimer mouvement de {str(move)}'})
        except Exception as e:
           return Response({"msg":'Probleme est servenu lors de suprrission de ce mouvement'})



@api_view(['PUT']) 
def updateMovement(request,id):
    if request.method=='PUT':
        req=request.data
        print(req)
        try:
               move=Movement.objects.get(id=id)
               move.dateMovement=req.get('dateMovement')
               move.typeLocation=req.get('typeLocation')
               move.depot=req.get('depot')
               move.designation=req.get('designation')
               move.qte=req.get('qte')
               move.ville=req.get('ville')
               move.lieu=req.get('lieu')
               move.matTrans=req.get('matTrans')
               move.condTrans=req.get('condTrans')
               move.observations=req.get('observations')
                
               move.save()

               return Response({'msg': f'Vous avez modifier details de {request.data.get("refMateriel")}'})
        except Exception as e:
            print(e)
            return Response({'msg':str(e)})           

#handling chargeaffaire

@api_view(['GET'])
def chargeAffaire(request):
    if request.method=='GET':
        charge=Chargesaffaire.objects.all()
        serializer=ChargesaffaireSerializer(charge,many=True)
        return Response(serializer.data)
#handling of reservisation

@api_view(['GET'])
def reservation(request):
    if request.method=='GET':
        reservations=Reservation.objects.all().order_by('dateReservation')
        serializer=ReservationSerializer(reservations,many=True)

    return Response(serializer.data)