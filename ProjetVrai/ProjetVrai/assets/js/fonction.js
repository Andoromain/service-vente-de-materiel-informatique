
function supprimerAchat(id){
	swal({
			title: "Etes- vous Sur?",
			text: "Si vous le supprimer , on ne peut pas le recuperer?",
			icon: "warning",
			buttons: true,
			dangerMode: true,
		}).then((willDelete) => {
			if (willDelete) {
				$.ajax({
					type:'GET',
					url:'ajax/form',
					data:({ value:id }),
					success:function($data,$textStatus,$XMLHtpRequest){
						swal({
							title: "",
							text: $data,
							icon: "success",
						}).then((willDelete) => {
							if (willDelete){
								document.location.reload();
							};
						});			
					},
					error:function(){
						swal({
								title: "",
								text: "Il y a erreur au serveur pour le moment!!",
								icon: "error",
						}).then((willDelete) => {
							if (willDelete){
								document.location.reload();
							};
						});
					}
				});
			};
		});
}
function modifierAchat(id,numMat,qte){
	$("#id").val(id);
	$("#numMat").val(numMat);
	$("#qte").val(qte);
}