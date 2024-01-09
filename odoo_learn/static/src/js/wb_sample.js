odoo.define("odoo_learn.WBSampleButton", function(require){
"use strict";

    const PosComponent = require("point_of_sale.PosComponent");
    const ProductScreen = require("point_of_sale.ProductScreen");
    const Registries = require("point_of_sale.Registries");
    const { useListener } = require("@web/core/utils/hooks");

    class WBSampleButton extends PosComponent {

        setup(){
            super.setup();
            useListener("click", this.wb_sample_button_click)
        }
        wb_sample_button_click(){
            console.log("Hello this is a sample button")
        }
    }

    WBSampleButton.template = "WBSampleButton";
    ProductScreen.addControlButton({
        component: WBSampleButton,
        position: ["before", "QederlineCustomerNotaButton"],
    });

    Registries.Component.add(WBSampleButton);

    return WBSampleButton;

});