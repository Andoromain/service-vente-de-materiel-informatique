$(document).ready(function(){
    $("#SuppressionEnseignant").click(function(){
        swal({
  title: "Etes- vous Sur?",
  text: "Si vous le supprimer , on ne peut pas le recuperer?",
  icon: "warning",
  buttons: true,
  dangerMode: true,
})
.then((willDelete) => {
  if (willDelete) {
    swal("Supprime avec succes!", {
      icon: "success",
    });}
        }
      )});
        
    $("#modalEn #modifierEn").click(function(){
        swal("Modification avec Success!!","","success");  
    });
 });    