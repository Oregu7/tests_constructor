var App = App ? App : {
	Views : {},
	Models : {},
	Collections : {}
};

App.Models.Settings = Backbone.Model.extend({
	defaults: {
		title: '',
		description: '',
		category: '',
		quest_count: 10,
		helps: false,
		timeCompl: 0,
		two_mark: 25,
		three_mark: 55,
		four_mark: 85
	}
});

App.Views.Settings = Backbone.View.extend({
	el: '#test_settings',

	initialize: function(){
		this.fields = {
			name: this.$el.find('input[name="title"]'),
			helps: this.$el.find('input[name="help"]'),
			timeCompl: this.$el.find('input[name="time"]'),
			description: this.$el.find('textarea[name="description"]'),
			category: this.$el.find('select[name="category"]'),
			quest_count: this.$el.find('input[name="quest_count"]'),
			marks: {
				two: this.$el.find('input[name="two_mark"]'),
				three: [this.$el.find('input[name="three_mark_b"]'), this.$el.find('input[name="three_mark"]')],
				four: [this.$el.find('input[name="four_mark_b"]'), this.$el.find('input[name="four_mark"]')],
				five: this.$el.find('input[name="five_mark_b"]')
			}
		};

		this.$el.find('.ui.header').transition('tada');
		this.fields.description.val(this.fields.description.attr('data-desc'))
	},

	events: {
		'mouseover .ui.header': 'scaleTransit',
		'click #create_test': 'create_test',
		'change input[name="two_mark"]': 'changeTwoMark',
		'change input[name="three_mark"]': 'changeThreeMark',
		'change input[name="four_mark"]': 'changeFourMark',
		'click #edit_test' : 'edit_test',
		'change input[name="quest_count"]': 'setQuestCount',
        'change input[name="time"]': 'setTime'
	},

	changeTwoMark: function(){
		var twoMark = Number(this.fields.marks.two.val())
		//значение должно быть больше 0 , но меньше максимального значения оценки 3
		if ( twoMark > 0 && twoMark < this.model.get('three_mark')){
			//обновляем данные в модели
			this.model.set({two_mark: twoMark});
			this.fields.marks.three[0].val(this.model.get('two_mark'));
		}else{
			//иначе записываем первоначальные данные
			this.fields.marks.two.val(this.model.get('two_mark'))
		}
	},

	changeThreeMark: function(){
		var threeMark = Number(this.fields.marks.three[1].val());

		if( threeMark > this.model.get('two_mark') && threeMark < this.model.get('four_mark')){
			this.model.set({three_mark: threeMark});
			this.fields.marks.four[0].val(threeMark)
		}else{
			this.fields.marks.three[1].val(this.model.get('three_mark'))
		}
	},

	changeFourMark: function(){
		var fourMark = Number(this.fields.marks.four[1].val());
		if (fourMark > this.model.get('three_mark') && fourMark < 100 ){
			this.model.set({four_mark: fourMark});
			this.fields.marks.five.val(fourMark);
		}else{
			this.fields.marks.four[1].val(this.model.get('four_mark'))
		}
	},

	scaleTransit: function(){
		this.$el.find('.ui.header').transition('pulse')
	},

	create_test: function(){
		if (this.fields.name.val().length == 0){
			swal("Ошибка!", 'Вы не указали название!', 'error')
		}else{
			this.model.set({
				title: this.fields.name.val(),
				description: this.fields.description.val(),
				helps: this.fields.helps.prop('checked'),
				category: this.fields.category.val()
			});

			$.post('/constructor/', this.model.toJSON(), function(data){
				if (!data.error){
					window.location.assign('/constructor/test/' + data.testID + '/questions/');
				}
			});
		}
	},

	edit_test:function(){
		var testID = $('#edit_test').attr('testID');

		if (this.fields.name.val().length == 0){
			swal("Ошибка!", 'Вы не указали название!', 'error')
		}else{
			this.model.set({
				title: this.fields.name.val(),
				description: this.fields.description.val(),
				timeCompl: this.fields.timeCompl.val(),
				helps: this.fields.helps.prop('checked'),
				two_mark: this.fields.marks.two.val(),
				three_mark: this.fields.marks.three[1].val(),
				four_mark: this.fields.marks.four[1].val(),
				category: this.fields.category.val(),
                quest_count: this.fields.quest_count.val()
			});

			$.post('', this.model.toJSON(), function(data){
				swal('Выполено!', data.success, 'success')
			});
		}	
	},

	setQuestCount: function(){
		var that = this;
		if (that.fields.quest_count.val() < 1){
			swal('Ошибка!', "Количество вопросов должно быть больше 0!", "error")
			that.fields.quest_count.val(that.model.get('quest_count'))
		}else{
			that.model.set('quest_count', that.fields.quest_count.val())
		}
	},

    setTime: function(){
        var that = this;
		if (that.fields.timeCompl.val() < 0){
			swal('Ошибка!', "Время не может быть меньше 0!", "error")
			that.fields.timeCompl.val(that.model.get('timeCompl'))
		}else{
			that.model.set('timeCompl', that.fields.timeCompl.val())
		}
    }
});

var testSettings = new App.Views.Settings({model: new App.Models.Settings()});
