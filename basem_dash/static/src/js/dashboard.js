/** @odoo-module */

import {registry} from '@web/core/registry';
const {Component, onWillStart, useState} = owl;
import {useService} from "@web/core/utils/hooks";

export class ProjectDashboard extends Component {
    setup() {
        this.action = useService("action");
        this.rpc = useService("rpc");

        // Initialize state for sales, leads, invoices, and bills
        this.state = useState({
            sales_count: 0,
            leads_count: 0,
            invoice_count: 0,
            bill_count: 0
        });

        // Fetch counts for sales, leads, invoices, and bills before rendering
        onWillStart(async () => {
            const [sales_result, leads_result, invoices_result, bills_result] = await Promise.all([
                this.rpc('/web/dataset/call_kw', {
                    model: 'sale.order',
                    method: 'search_count',
                    args: [[]],
                    kwargs: {}
                }),
                this.rpc('/web/dataset/call_kw', {
                    model: 'crm.lead',
                    method: 'search_count',
                    args: [[]],
                    kwargs: {}
                }),
                this.rpc('/web/dataset/call_kw', {
                    model: 'account.move',
                    method: 'search_count',
                    args: [[['move_type', '=', 'out_invoice']]],  // Invoices
                    kwargs: {}
                }),
                this.rpc('/web/dataset/call_kw', {
                    model: 'account.move',
                    method: 'search_count',
                    args: [[['move_type', '=', 'in_invoice']]],  // Bills
                    kwargs: {}
                })
            ]);

            // Update state with results
            this.state.sales_count = sales_result;
            this.state.leads_count = leads_result;
            this.state.invoice_count = invoices_result;
            this.state.bill_count = bills_result;
        });
    }

    _onClickSales() {
        this.action.doAction({
            name: "Sales",
            type: 'ir.actions.act_window',
            res_model: 'sale.order',
            views: [[false, 'list'], [false, 'form']],
            context: {create: false},
            target: 'current'
        });
    }

    _onClickLeads() {
        this.action.doAction({
            name: "CRM Leads",
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
            context: {create: false},
            target: 'current'
        });
    }

    _onClickInvoices() {
        this.action.doAction({
            name: "Invoices",
            type: 'ir.actions.act_window',
            res_model: 'account.move',
            views: [[false, 'list'], [false, 'form']],
            context: {create: false, search_default_out_invoice: 1},
            domain: [['move_type', '=', 'out_invoice']],
            target: 'current'
        });
    }

    _onClickBills() {
        this.action.doAction({
            name: "Bills",
            type: 'ir.actions.act_window',
            res_model: 'account.move',
            views: [[false, 'list'], [false, 'form']],
            context: {create: false, search_default_in_invoice: 1},
            domain: [['move_type', '=', 'in_invoice']],
            target: 'current'
        });
    }
}

ProjectDashboard.template = "ProjectDashBoardMain";
registry.category("actions").add("sales_dashboard_main", ProjectDashboard);
