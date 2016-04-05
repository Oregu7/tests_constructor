TestMVC.module('Entities', function(Entities, TestApp, Backbone, Marionette, $, _){
    Entities.Test = Backbone.Model.extend({});

    Entities.TestCollection = Backbone.Model.extend({
        model: TestApp.Test,
        url: '/api/tests/'
    });

    var tests;
    var initializeTests = function(){
        tests = new Entities.TestCollection();
        tests.fetch();
    }

    var API = {
        getTestsEntities: function(){
            if (tests === undefined){
                initializeTests();
            }

            return tests;
        }
    };

    TestMVC.reqres.setHandler('tests:all', function(){
        return API.getTestsEntities()
    })
})
