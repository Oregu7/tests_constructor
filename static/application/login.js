var App = App ? App : {
	Views : {},
	Models : {},
	Collections : {}
};

App.Models.Login = Backbone.Model.extend({
	defaults : {
		login: '',
		password: '',
		remember : false
	},

    validate: function(attrs){
        if (attrs.login.length < 4 || attrs.login.length > 20){
            return {field: 'login', msg: 'Логин от 4 до 20 символов'}
        };

        if (attrs.password.length < 6 || attrs.password.length > 30){
            return {field: 'password', msg: 'Пароль от 6 до 30 символов'}
        };
    },

	urlRoot: '/login/'

});

App.Views.Login = Backbone.View.extend({
	el: $('#login_form'),
    initialize: function(){
        console.log('loginView is create');
        this.fields = {
           login : this.$el.find('input[name="login"]'),
           password : this.$el.find('input[name="password"]'),
           remember : this.$el.find('input[name="remember"]')
        };

        this.model.on('invalid', this.errModel, this)
        this.model.on('change', this.login_user, this)
    },
    events:{
        'click button' : 'login_in',
        'submit': 'submit_form'
    },

    login_in: function(){
        this.model.set({
            login: this.fields.login.val(),
            password: this.fields.password.val(),
            remember: this.fields.remember.prop('checked')
        },{validate:true});
    },

    login_user:function(){
    	$.post(this.model.urlRoot, this.model.toJSON(), function(data){
    		if (!data.error){
    			window.location.assign('/')
    		}else{
    			swal('Ошибка', data.error, 'error')
    		}
    	})
    },

    submit_form: function(){
        return false;
    },

    errModel:function(model, error){
        this.fields[error.field].parents('.field').addClass('error');
        this.fields[error.field].parents('.field').find('.label').remove();
        this.fields[error.field].parents('.field').append('<div class="ui pointing red basic label">' +error.msg+ '</div>');
    }
});

var loginView = new App.Views.Login({model: new App.Models.Login()})



