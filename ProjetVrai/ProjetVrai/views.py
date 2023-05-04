# -*- coding : utf-8 -*-
from django.shortcuts import render,redirect,HttpResponse
from ProjetVrai.models import client,materiel,achat 
from ProjetVrai.settings import BASE_DIR
import os

def acceuil(requete):
    return render(requete,'index.html', content_type='text/html')
def welcome(requete,ok=""):
    if 'modifAchat' in requete.POST:
        #code modification achat
        
        idmc=requete.POST['id']
        numMat=requete.POST['numMat']
        qte=requete.POST['qte']
        
        mod=achat.objects.get(id=idmc)
        mod.numMat=numMat
        mod.qte=qte
        mod.save()
        
        logged_user_id=requete.session["logged_user_id"]
        logged_user=client.objects.get(numClient=logged_user_id)
        acha=achat.objects.filter(numClient=logged_user.numClient);
        mat=materiel.objects.all()
        return render(requete,'visiteur/welcome.html',{'logged_user':logged_user,'materiels':mat,
                                                       'lenMat':len(mat),'achats':acha,'ok':ok,'ko':'' })
    if requete.method=="GET":
        if "logged_user_id" in requete.session :
            logged_user_id=requete.session["logged_user_id"]
            logged_user=client.objects.get(numClient=logged_user_id)
            acha=achat.objects.filter(numClient=logged_user.numClient);
            mat=materiel.objects.all()
            return render(requete,'visiteur/welcome.html',{'logged_user':logged_user,'materiels':mat,
                                                       'lenMat':len(mat),'achats':acha,'ok':ok,'ko':'' })
        else:
            return redirect("/login")
    q=False
    if "numMat" in requete.POST or "qte" in requete.POST or "dateAchat":
        mat=materiel.objects.all()
        for mater in mat:
            if requete.POST["numMat"] == mater.numMat:
                unmateriel=materiel.objects.get(numMat=requete.POST["numMat"])
               
                qte=requete.POST["qte"]
                qte=int(qte)
                if(unmateriel.Stock<qte):
                    if "logged_user_id" in requete.session :
                        logged_user_id=requete.session["logged_user_id"]
                        logged_user=client.objects.get(numClient=logged_user_id)
                        ko="Le materiel que vous voulez achaté est en manque de stock"
                        acha=achat.objects.filter(numClient=logged_user.numClient);
                        mat=materiel.objects.all()
                        return render(requete,'visiteur/welcome.html',{'logged_user':logged_user,'materiels':mat,
                                                       'lenMat':len(mat),'achats':acha,'ok':'','ko':ko})
                    else:   
                        return redirect("/login")
                else:
                    sauvegarde=unmateriel.Stock-qte
                    materiels=materiel.objects.get(numMat=requete.POST["numMat"])
                    materiels.Stock=sauvegarde
                    materiels.save()
                    mate=achat(numClient=requete.POST["numClient"],numMat=requete.POST["numMat"],qte=requete.POST["qte"])
                    mate.save()
                    q=True    
        if q==True:
            if "logged_user_id" in requete.session :
                logged_user_id=requete.session["logged_user_id"]
                logged_user=client.objects.get(numClient=logged_user_id)
                ok="Votre achat a été effectué!"
                acha=achat.objects.filter(numClient=logged_user.numClient);
                mat=materiel.objects.all()
                return render(requete,'visiteur/welcome.html',{'logged_user':logged_user,'materiels':mat,
                                                       'lenMat':len(mat),'achats':acha,'ok':ok ,'ko':''})
            else:   
                return redirect("/login")
        else:
            if "logged_user_id" in requete.session :
                logged_user_id=requete.session["logged_user_id"]
                logged_user=client.objects.get(numClient=logged_user_id)
                ko="Nous n'avons pas encore le materiel que vous voulez acheté!"
                acha=achat.objects.filter(numClient=logged_user.numClient);
                mat=materiel.objects.all()
                return render(requete,'visiteur/welcome.html',{'logged_user':logged_user,'materiels':mat,
                                                       'lenMat':len(mat),'achats':acha,'ok':'','ko':ko })
            else:   
                return redirect("/login")             
    else:           
        if "logged_user_id" in requete.session :
            logged_user_id=requete.session["logged_user_id"]
            logged_user=client.objects.get(numClient=logged_user_id)
            print(ok)
            acha=achat.objects.filter(numClient=logged_user.numClient);
            mat=materiel.objects.all()
            return render(requete,'visiteur/welcome.html',{'logged_user':logged_user,'materiels':mat,
                                                       'lenMat':len(mat),'achats':acha,'ok':ok,'ko':'' })
        else:
            return redirect("/login")                  
    
def login(requete):
    if len(requete.POST)>0:
        if 'numero' not in requete.POST or 'password' not in requete.POST:
            error="veuillez entrez votre numero et un mot de passe!"
            return render(requete,'login.html',{'error':error})
        else:
            numero=requete.POST["numero"]
            password=requete.POST["password"]
            result=client.objects.filter(numClient=numero,password=password)
            if len(result)!=1:
                error="Le mot de passe ou l'adresse electronique est invalide"
                return render(requete,'login.html',{'error':error})
            else:
                requete.session["logged_user_id"]=requete.POST["numero"]
                return redirect('/welcome')
    else:
        return render(requete,'login.html')
            
def register(requete):
    
    if len(requete.POST)>0:
        
        if 'numero' not in requete.POST or "nom" not in requete.POST or "password1" not in requete.POST or "password2" not in requete.POST:
            error="veuillez entrez une numero , nom et un mot de passe!"
            return render(requete,'register.html',{'error':error})
        else:
            numero=client.objects.filter(numClient=requete.POST["numero"])
                    
            if len(numero)==1:
                error="Le numero saisi est deja enregistre par un autre client!"
                return render(requete,'register.html',{'error':error})
            else:
                if requete.POST["password1"]==requete.POST["password2"]:
                    num=client(numClient=requete.POST["numero"],nomClient=requete.POST["nom"],password=requete.POST["password1"])
                    num.save()
                    requete.session["logged_user_id"]=requete.POST["numero"]
                    return redirect('/welcome')
                else:
                    error="Les deux mot de passe saisi ne sont pas les memes!"
                    return render(requete,'register.html',{'error':error}) 
    else:
        return render(requete,'register.html')    
    
    return render(requete,'register.html')
def logout(requete):
    requete.session.flush()
    return redirect("/login")
def ajax_form(requete):
    html_to_return=""
    if 'value' in requete.GET:
        idm=requete.GET["value"]
        sauve=achat.objects.get(id=idm);
        sauve.delete()
        html_to_return="L'achat a ete supprime avec succes"
        return HttpResponse(html_to_return)
    else:
        html_to_return="Erreur"
        return HttpResponse(html_to_return)