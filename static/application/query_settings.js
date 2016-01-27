var App = App ? App : {
	Views : {},
	Models : {},
	Collections : {}
};

App.Models.Answer = Backbone.Model.extend({
	defaults: {
		text: '',
		correct: false
	}
});

App.Models.Query = Backbone.Model.extend({
	defaults:{
		text: '',
		help: '',
		point: 1,
		time: 5
	}
})

App.Collections.Answers = Backbone.Collection.extend({
	model: App.Models.Answer
});

App.Views.Answer = Backbone.View.extend({
	tagName: 'tr',
	template: _.template($('#answerTemplate').html()),
	initialize: function(){
		this.model.on('destroy', this.remove, this);
		this.render();
	},

	events: {
		'click .circular.button': 'deleteAnswer',
		'change input:text' : 'setText',
		'click .ui.checkbox' : 'setCorrect'
	},

	render: function(){
		this.$el.html(this.template(this.model.toJSON()));
		this.$el.find('.ui.checkbox').checkbox();
		return this
	},

	setText: function(){
		this.model.set({
			text: this.$el.find('input:text').val()
		})
	},

	setCorrect: function(){
		this.model.set({
			correct: this.$el.find('input:checkbox').prop('checked')
		})
	},

	deleteAnswer: function(){
		this.model.destroy()
	}
});

App.Views.Query = Backbone.View.extend({
	el: '#query_settings',
	initialize: function(){
		this.collection.on('add', this.addItem, this);
		this.collection.on('reset', this.tbodyEmpty, this)
	},

	events: {
		'click #add_answ' : 'addAnswer',
		'click #save_query' : 'saveQuery',
		'change textarea[name="text_query"]' : 'setQueryText',
		'change textarea[name="text_helps"]' : 'setHelp',
		'change input[name="point"]' : 'setPoint',
		'change input[name="time"]' : 'setTime'
	},

	addAnswer: function(){
		this.collection.add(new App.Models.Answer())
	},

	addItem: function(answer){
		this.$el.find('tbody').append(new App.Views.Answer({model: answer}).el)
	},

	tbodyEmpty: function(){
		this.$el.find('tbody').empty()
	},

	setQueryText: function(){
		this.model.set({text: this.$el.find('textarea[name="text_query"]').val()})
	},

	setHelp: function(){
		this.model.set({help: this.$el.find('textarea[name="text_helps"]').val()})
	},

	setPoint: function(){
		this.model.set({point: this.$el.find('input[name="point"]').val()})
	},

	setTime: function(){
		this.model.set({time: this.$el.find('input[name="time"]').val()})
	},

	saveQuery: function(){
		var url = '/constructor/test/' + this.$el.find('#save_query').attr('data-testID') + '/questions/add/';
		data = this.model.toJSON();
		data['answers'] = JSON.stringify(this.collection.toJSON());

		$.post(url, data, $.proxy(function(response){
			if (response.complite){
				swal('Сохранено!', 'Данный вопрос был успешно сохранен', 'success');
				this.collection.reset();
				this.model.set({
					text: '',
					help: '',
					point: 1,
					time: 5
				});

				this.$el.find('textarea').val('');
				this.$el.find('input').val('');
			}
		},this))
	}
});

var answersView = new App.Views.Query({
	collection: new App.Collections.Answers(),
	model: new App.Models.Query
})