var App = App ? App : {
	Views : {},
	Models : {},
	Collections : {}
};

App.Models.Settings = Backbone.Model.extend({
	defaults: {
		title: '',
		description: '',
		helps: false,
		timeCompl: false,
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
			marks: {
				two: this.$el.find('input[name="two_mark"]'),
				three: [this.$el.find('input[name="three_mark_b"]'), this.$el.find('input[name="three_mark"]')],
				four: [this.$el.find('input[name="four_mark_b"]'), this.$el.find('input[name="four_mark"]')],
				five: this.$el.find('input[name="five_mark_b"]')
			}
		};

		this.$el.find('.ui.header').transition('tada');
	},

	events: {
		'mouseover .ui.header': 'scaleTransit',
		'click #create_test': 'create_test',
		'change input[name="two_mark"]': 'changeTwoMark',
		'change input[name="three_mark"]': 'changeThreeMark',
		'change input[name="four_mark"]': 'changeFourMark'
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
		if (this.fields.name.val().length <= 4){
			Lobibox.notify('error', {
				icon: false,
				sound: false,
				delay: 7000,
				title:'Ошибка',
				msg: 'Название теста слишком короткое, должно быть больше 4 символов'
			});
		}else{
			this.model.set({
				title: this.fields.name.val(),
				description: this.$el.find('textarea[name="description"]').val(),
				timeCompl: this.fields.timeCompl.prop('checked') ? 1 : 0,
				helps: this.fields.helps.prop('checked')
			});

			$.post('/constructor/', this.model.toJSON(), function(data){
				if (!data.error){
					window.location.assign('/constructor/test/' + data.testID + '/');
				}
			});
		}
	}
});

var testSettings = new App.Views.Settings({model: new App.Models.Settings()});
