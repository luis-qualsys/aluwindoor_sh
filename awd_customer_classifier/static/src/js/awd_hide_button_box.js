odoo.define('fer_stock_compute_sourcing.fer_hide_edit_button.js', function (require) {

    const FormController = require('web.FormController');

    FormController.include({
        decideToShowButtons: function(){
            console.log('innerDecideToShowButtons')
            // console.log('Decide This', this.modelName)
            if (this.modelName === "res.partner"){
                // console.log('Model', this.modelName)
                // console.log('THIS', this)
                // console.log('Decide Model Local', this.model.localData)
                const dataModel = this.model.localData
                const contextModel = this.model.loadParams.context
                const login_user = contextModel.uid
                // console.log(dataModel)
                let creator_user = dataModel['res.partner_1'].data.user_id
                let user_final = dataModel[creator_user].res_id
                console.log(login_user, user_final)
                // console.log(dataModel['res.partner_1'].data.user_id)
                // const user = dataModel[dataModel['res.partner_1'].data.user_id]
                // console.log('USER', user.res_id)
                if (login_user !== user_final){
                    console.log('Hide button')
                    $("div").find('.oe_button_box').hide()
                } else {
                    console.log('Show button')
                    $("div").find('.oe_button_box').show()
                }
            }
        },
        renderButtons: function(){
            // console.log('render buttons');
            this._super.apply(this, arguments);
            this.decideToShowButtons();
        },
        reload: function(){
            var self = this;
            // console.log('reload record');
            return this._super.apply(this, arguments).then(function(res){
                self.decideToShowButtons();
                return res;
            });
        },
        saveRecord: function() {
            // console.log('save record');
            var self = this;
            return this._super.apply(this, arguments).then(function(res){
                self.decideToShowButtons();
                return res;
            })
        }
    });
});