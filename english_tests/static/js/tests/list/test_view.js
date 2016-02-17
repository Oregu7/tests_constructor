TestMVC.module('TestsApp.List', function(List, TestMVC, Backbone, Marionette, $, _){
    List.Test = Marionette.ItemView.extend({
        tagname:"a",
        className:"collection-item"
    });

    List.TestsView = Marionette.CollectionView.extend({
        className:"collection",
        childView: List.Test
    })
});
