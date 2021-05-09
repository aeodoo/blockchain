odoo.define("odoo_addons_blockchain_proxy.client", function(require) {
    "use strict";

    var Widget = require("web.Widget");
    var publicWidget = require("web.public.widget");
    var AuthMetamask = require("auth_metamask.client");

    var AddressForm = Widget.extend({
        start: function() {
            var self = this;
            var res = this._super.apply(this.arguments).then(function() {
                $(".get-metamask-address")
                    .off("click")
                    .click(function(ev) {
                        self.on_click(ev);
                    });
            });
            return res;
        },
        on_click: async function(ev) {
            ev.preventDefault();
            ev.stopPropagation();
            var authMetamask = new AuthMetamask();
            var coinbase = await authMetamask.get_coinbase();
            var public_address = coinbase.toLowerCase();
            $("#public_address").val(public_address);
        },
    });

    publicWidget.registry.AddressFormInstance = publicWidget.Widget.extend({
        selector: ".get-metamask-address",
        start: function() {
            var def = this._super.apply(this, arguments);
            this.instance = new AddressForm(this);
            return Promise.all([def, this.instance.attachTo(this.$el)]);
        },
        destroy: function() {
            this.instance.setElement(null);
            this._super.apply(this, arguments);
            this.instance.setElement(this.$el);
        },
    });

    return AddressForm;
});
