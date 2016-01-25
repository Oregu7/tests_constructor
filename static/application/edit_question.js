var App = App ? App : {
	Views : {},
	Models : {},
	Collections : {}
};

App.Models.Answer = Backbone.Model.extend({
	defaults: {
		text: '',
		correct: false
	},

	urlRoot: '/constructor/question/' + $('#query_settings').attr('data-question') + '/'
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
		this.model.save({
			text: this.$el.find('input:text').val()
		})
	},

	setCorrect: function(){
		this.model.save({
			correct: this.$el.find('input:checkbox').prop('checked')
		});
	},

	deleteAnswer: function(){
		this.model.destroy({
			success: function(model, response){
        		console.log(response.msg);
      		}
		})
	}
});

App.Views.Query = Backbone.View.extend({
	el: '#query_settings',
	initialize: function(){
		var that = this;
		this.question = Number(this.$el.attr('data-question'));
		this.test = Number(this.$el.attr('data-test'));

		this.collection.on('add', this.addItem, this);
		this.collection.on('reset', this.tbodyEmpty, this);
		//Подтягиваем ответы
		this.collection.url = '/constructor/question/'+this.question+'/';
		this.collection.fetch();
		//Подтягиваем вопрос
		this.model.url = '/constructor/test/'+this.test+'/questions/edit/'+this.question+'/'
		this.model.save(null,{
			success:function(model, response){
				that.$el.find('textarea[name="text_query"]').val(model.get('text'));
				that.$el.find('textarea[name="text_helps"]').val(model.get('help'));
				that.$el.find('input[name="point"]').val(model.get('point'));
				that.$el.find('input[name="time"]').val(model.get('time'));
			}
		});
	},

	events: {
		'click #add_answ' : 'addAnswer',
		'click #back' : 'back_to_test',
		'change textarea[name="text_query"]' : 'setQueryText',
		'change textarea[name="text_helps"]' : 'setHelp',
		'change input[name="point"]' : 'setPoint',
		'change input[name="time"]' : 'setTime'
	},

	addAnswer: function(){
		answer = new App.Models.Answer();
		answer.save();
		this.collection.add(answer);
	},

	addItem: function(answer){
		this.$el.find('tbody').append(new App.Views.Answer({model: answer}).el)
	},

	tbodyEmpty: function(){
		this.$el.find('tbody').empty()
	},

	setQueryText: function(){
		this.model.save({text: this.$el.find('textarea[name="text_query"]').val()})
	},

	setHelp: function(){
		this.model.save({help: this.$el.find('textarea[name="text_helps"]').val()})
	},

	setPoint: function(){
		this.model.save({point: this.$el.find('input[name="point"]').val()})
	},

	setTime: function(){
		this.model.save({time: this.$el.find('input[name="time"]').val()})
	},

	back_to_test:function(){
		window.location.assign('/constructor/test/'+this.test+'/questions/')
	}

	
});

var answersView = new App.Views.Query({
	collection: new App.Collections.Answers(),
	model: new App.Models.Query
})