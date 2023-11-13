odoo.define("odoo_learn.WBSampleButton", function(require){
"use strict";

    const PosComponent = require("point_of_sale.PosComponent");
    const ProductScreen = require("point_of_sale.ProductScreen");
    const Registries = require("point_of_sale.Registries");

    class WBSampleButton extends PosComponent {

    }

    WBSampleButton.template = "WBSampleButton";
    ProductScreen.addControlButton({
        component: WBSampleButton,
        position: ["before", "QederlineCustomerNotaButton"],
    });

    Registries.Component.add(WBSampleButton);

    return WBSampleButton;

});