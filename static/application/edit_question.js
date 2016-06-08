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
		point: 1
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
        var that = this;
        var text = that.$el.find('input:text');
        if(!text.val().length){
            swal('Ошибка', 'Поле текст ответа не может быть пустым!', 'error');
            text.val(that.model.get('text'));
        }else{
            that.model.save({
			    text: text.val()
		    })
        }

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
			}
		});
	},

	events: {
		'click #add_answ' : 'addAnswer',
        'click #delete_answers': 'deleteAnswers',
		'click #back' : 'back_to_test',
		'change textarea[name="text_query"]' : 'setQueryText',
		'change textarea[name="text_helps"]' : 'setHelp',
		'change input[name="point"]' : 'setPoint'
	},

	addAnswer: function(){
		answer = new App.Models.Answer();
		answer.save();
		this.collection.add(answer);
	},

    deleteAnswers: function(){
        var answers_array = this.collection.models.slice();
        _.each(answers_array, function(answer){
            answer.destroy();
        })
    },

	addItem: function(answer){
		this.$el.find('tbody').append(new App.Views.Answer({model: answer}).el)
	},

	tbodyEmpty: function(){
		this.$el.find('tbody').empty()
	},

	setQueryText: function(){
        var text = this.$el.find('textarea[name="text_query"]');
        if(text.val().length < 5){
            swal('Ошибка', 'Минимальное количество символов в тексте вопроса - 5', 'error');
            text.val(this.model.get('text'));
        }else{
            this.model.save({text: text.val()});
        }

	},

	setHelp: function(){
		this.model.save({help: this.$el.find('textarea[name="text_helps"]').val()})
	},

	setPoint: function(){
        var point = this.$el.find('input[name="point"]');
        if(point.val() <= 0){
            swal('Ошибка!',"Балл не может быть меньше или равен 0", 'error');
            point.val(this.model.get('point'));
        }else{
            this.model.save({point: point.val()});
        }

	},

	back_to_test:function(){
        var correct_answer = false;
        var empry_text_answer = false;
		data = this.model.toJSON();
		data['answers'] = this.collection.toJSON();

        _.each(data.answers, function(answer){
            if(answer.text.length){
                empry_text_answer = true;
            }

            if(answer.correct){
                correct_answer = true;
            }
        })

        if(data.text.length < 5){
            swal('Ошибка', 'Минимальное количество символов в тексте вопроса - 5', 'error');
        }else if(data.answers.length == 0){
            swal('Ошибка', 'Вы не добавиил ни одного ответа', 'error');
        }else if(data.answers.length < 2){
            swal('Ошибка', 'Минимальное количество ответов - 2', 'error');
        }else if(!empry_text_answer){
            swal('Ошибка', 'Вы не заполнили текст овета в одном из ответов', 'error');
        }else if(!correct_answer){
            swal('Ошибка', 'Вы не выбрали ни одного правильного ответа', 'error');
        }else{
           window.location.assign('/constructor/test/'+this.test+'/questions/');
        }
	}

	
});

var answersView = new App.Views.Query({
	collection: new App.Collections.Answers(),
	model: new App.Models.Query
})