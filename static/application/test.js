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
App.Models.Answer = Backbone.Model.extend({
	defaults: {
		selection: false
	}
})
App.Collections.Answers = Backbone.Collection.extend({
	model: App.Models.Answer
})

App.Views.Question = Backbone.View.extend({
	tagName: 'div',
	className: 'ui segment',
	template: _.template('<%- text %>'),

	initialize: function(){
		this.model.on('change', this.render, this)
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
		this.model.set('selection',answer)
	},

	render: function(){
		this.$el.html(this.template(this.model.toJSON()));
		this.$el.find('.ui.checkbox').checkbox();
		return this
	}
})

App.Views.Answers = Backbone.View.extend({
	className: 'ui large list',
	initialize: function(){
		this.collection.on('reset', this.render, this)
		this.render()
	},
	render: function(){
		var that = this;
		that.$el.empty();

		_.each(that.collection.models, function(model){
			var answer = new App.Views.Answer({model: model})
			that.$el.append(answer.el)
		})

		return this;
	}
})

App.Views.Test = Backbone.View.extend({
	el: '#content',
	template: _.template($('#next_tmpl').html()),
	result_template: _.template($('#result_tmpl').html()),

	initialize: function(){
		this.questionModel =  new App.Models.Question;
		this.answersCollection =  new App.Collections.Answers;
	},

	events: {
		'click #start': 'start_test',
		'click #next_quest': 'next_quest',
		'click #help' : 'show_help'
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
						var test = that.$el.find('#test');
						test.empty()
						//Вопрос
						test.append(new App.Views.Question({
							model: that.questionModel.set(data.quest)
						}).el)
						//Ответы
						that.answersCollection.reset(data.answers)
						
						test.append(new App.Views.Answers({
							collection: that.answersCollection
						}).el)

						that.$el.append(that.template())
						//если имя не указано
						if (!data.name){
							swal({
								title: "Тест загружен!",   
								text: "Введите свою фамилию:",   
								type: "input",   
								showCancelButton: false,   
								closeOnConfirm: false,   
								animation: "slide-from-top",   
								inputPlaceholder: "Ваша фамилия.." 
								}, 
								function(inputValue){
									inputValue = inputValue.replace(/\s+/g, '');

									if (inputValue === false) return false;      
									if (inputValue.length == 0) {     
										swal.showInputError("Вы должны ввести что-нибудь");     
										return false   
									}else{
										$.post('/tests/set_name/', {user: inputValue}, function(response){
											swal("Отлично!", inputValue + ", можете начинать тестирование", "success");
											//проверяем нужен ли нам таймер
											that.check_timer() 
										});	
									}      
									
							});

						}else{
							swal("Отлично!", "Тест загружен", "success")
							that.check_timer() 
						}
					})
				}, 2000);
			});
	},

	next_quest: function(){
		var that = this;
		var selection = false;

		_.each(that.answersCollection.models, function(answer){
			if (answer.get('selection')){
				selection = true
			}
		})

		if (selection || that.model.get('time')){
			var data = {'answers' : JSON.stringify(that.answersCollection.toJSON())}
			$.post('/tests/next/', data, function(response){
				var quest_data = JSON.parse(response)
				if (quest_data.test_result){
					console.log(quest_data)
					that.$el.empty()
					that.$el.html(that.result_template(quest_data))
				}else{
					that.questionModel.set(quest_data.quest)
					that.answersCollection.reset(quest_data.answers)
					that.check_timer();
				}
			});
		}else{
			swal('Ошибка!', "Выберите хотя бы 1 правильный ответ", "error")
		}
	},

	check_timer: function(){
		var that = this;

		if (timer) {
			clearInterval(that.timer);
			clearTimeout(that.stopTimer);
		}

		if (that.questionModel.get('time')){
			var minutes = that.questionModel.get('time'),
				seconds = 0;

			that.timer = setInterval(function(){
				if (seconds >= 0 && seconds < 10 ){
					that.$el.find('#timer').html(minutes + " : 0" + seconds)
				}else{
					that.$el.find('#timer').html(minutes + " : " + seconds)
				}
				
				if (seconds == 0 ){
					minutes -= 1;
					seconds = 59
				}else{
					seconds -= 1;
				}
			}, 1000)

			that.stopTimer = setTimeout(function(){
				clearInterval(timer);
				//Время заканчивается
				that.model.set('time', true);
				//следующий вопрос
				that.next_quest();

			}, that.questionModel.get('time') * 60 * 1000)
		}
	},

	show_help: function(){
		var that = this;
		if (that.questionModel.get('help') && that.questionModel.get('help').length > 0){
			swal('Подсказка', that.questionModel.get('help'), 'info')
		}else{
			swal('Подсказка', 'В данном тесте или вопросе не предусмотрены', 'error')
		}
	}
});

var Test = new App.Views.Test({
	model : new App.Models.Test({
		time: false
	})
})