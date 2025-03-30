/* @odoo-module */

import { Component, useState, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class ListViewAction extends Component {
    static template = "app_one.listView";

    setup() {
        this.state = useState({ 'records': [] });
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        this.loadRecords();

        this.intervalId = setInterval(() => {this.loadRecords();}, 3000);
        onWillUnmount(() => {clearInterval(this.intervalId);});
    };

//    async loadRecords() {
//        const result = await this.orm.searchRead("property.model", [], []);
//        console.log(result);
//        this.state.records = result;
//    }

    async loadRecords(){
        const result = await this.rpc("/web/dataset/call_kw", {
            model: "property.model",
            method: "search_read",
            args: [[]],
            kwargs: {fields: ['id', 'name', 'postcode', 'date_available']},
            });
        console.log(result);
        this.state.records = result;
    };

    async createRecord() {
        await this.rpc("/web/dataset/call_kw", {
            model: "property.model",
            method: "create",
            args: [{name: "New Property", postcode: "12345", date_available: "2023-01-01"}],
            kwargs: {},
           })
        this.loadRecords();
    };

    async deleteRecord(recordId) {
        await this.rpc("/web/dataset/call_kw", {
            model: "property.model",
            method: "unlink",
            args: [recordId],
            kwargs: {},
           })

        this.loadRecords();
    };

};
registry.category("actions").add("app_one.action_list_view", ListViewAction);