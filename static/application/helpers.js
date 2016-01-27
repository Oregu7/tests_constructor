function model_to_json(model){
	return JSON.parse(model.replace(/&quot;/g,"\""))
}