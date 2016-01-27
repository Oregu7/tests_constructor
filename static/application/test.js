var App = App ? App : {
	Views : {},
	Models : {},
	Collections : {}
};

App.Models.Test = Backbone.Model.extend({
	defaults: {
		help: false,
		time: false,
	}
});

App.Models.Question = Backbone.Model.extend()
App.Models.Answer = Backbone.Model.extend()
App.Collections.Answers = Backbone.Collection.extend({
	model: App.Models.Answer
})

App.Views.Question = Backbone.View.extend({
	tagName: 'div',
	className: 'ui segment',
	template: _.template('<%- text %>'),

	initialize: function(){
		this.render()
	},

	render: function(){
		this.$el.html(this.template(this.model.toJSON()))
		return this
	}
})

App.Views.Answer = Backbone.View.extend({
	className: 'item',
	template: _.template($('#answer_tmpl').html()),
	initialize: function(){
		this.render()
	},

	events: {
		'change input[type="checkbox"]' : 'setAnswer'
	},

	setAnswer: function(){
		var answer = this.$el.find('input[type="checkbox"]').prop('checked')
		this.model.set({answer: answer})
		console.log(this.model.toJSON())
	},

	render: function(){
		this.$el.html(this.template(this.model.toJSON()));
		this.$el.find('.ui.checkbox').checkbox();
		return this
	}
})

App.Views.Answers = Backbone.View.extend({
	className: 'ui selection list',
	initialize: function(){
		this.render()
	},
	render: function(){
		var that = this;

		_.each(that.collection.models, function(model){
			var answer = new App.Views.Answer({model: model})
			that.$el.append(answer.el)
		})

		return this;
	}
})

App.Views.Test = Backbone.View.extend({
	el: '#content',
	initialize: function(){
		this.questionModel =  new App.Models.Question,
		this.answersCollection =  new App.Collections.Answers
	},

	events: {
		'click #start': 'start_test'
	},

	start_test: function(){
		var test = Number(this.$el.find('#start').attr('data-test'));
		var that = this;

		swal({
			title: 'Начать тестирование',
			text: 'Вы точно хотите начать тест?',
			type: 'info',
			confirmButtonColor: "#DD6B55",
			confirmButtonText: 'Да, начать!',
			cancelButtonText: 'Нет, не надо!',
			showCancelButton: true,
			closeOnConfirm: false,   
			showLoaderOnConfirm: true,
			},

			function(){
				setTimeout(function(){
					$.get('/tests/' + test + '/', {}, function(response){
						var data = JSON.parse(response);
						that.$el.empty()
						//Вопрос
						that.$el.append(new App.Views.Question({
							model: that.questionModel.set(data.quest)
						}).el)
						//Ответы
						that.answersCollection.reset(data.answers)
						
						that.$el.append(new App.Views.Answers({
							collection: that.answersCollection
						}).el)

						swal("Вопрос загружен");
					})
				}, 2000);
			});
	}
});

var Test = new App.Views.Test({
	model : new App.Models.Test
})