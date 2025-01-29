/** @odoo-module */

import {registry} from '@web/core/registry';
const {Component, onWillStart, useState} = owl;
import {useService} from "@web/core/utils/hooks";

export class ProjectDashboard extends Component {
    setup() {
        this.action = useService("action");
        this.rpc = useService("rpc");

        // Initialize state for all dashboard elements
        this.state = useState({
            sales_count: 0,
            leads_count: 0,
            invoice_count: 0,
            bill_count: 0,
            customer_count: 0,
            vendor_count: 0,
            purchase_count: 0,
            rfq_count: 0,
            quotation_count: 0,
            pipeline_count: 0,
            sales_team_count: 0
        });

        // Fetch counts for all sections before rendering
        onWillStart(async () => {
            const [
                sales_result, leads_result, invoices_result,
                bills_result, customers_result, vendors_result,
                purchase_result, rfq_result, quotation_result,
                pipeline_result, sales_team_result
            ] = await Promise.all([
                this.rpc('/web/dataset/call_kw', {
                    model: 'sale.order',
                    method: 'search_count',
                    args: [[['state', '=', 'sale']]],  // Only confirmed Sales Orders
                    kwargs: {}
                }),
                this.rpc('/web/dataset/call_kw', {
                    model: 'crm.lead',
                    method: 'search_count',
                    args: [[['type', '=', 'lead']]],
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
                }),
                this.rpc('/web/dataset/call_kw', {
                    model: 'res.partner',
                    method: 'search_count',
                    args: [[['customer_rank', '>', 0]]],  // Customers
                    kwargs: {}
                }),
                this.rpc('/web/dataset/call_kw', {
                    model: 'res.partner',
                    method: 'search_count',
                    args: [[['supplier_rank', '>', 0]]],  // Vendors
                    kwargs: {}
                }),
                this.rpc('/web/dataset/call_kw', {
                    model: 'purchase.order',
                    method: 'search_count',
                    args: [[['state', '=', 'purchase']]],  // Confirmed Purchase Orders
                    kwargs: {}
                }),
                this.rpc('/web/dataset/call_kw', {
                    model: 'purchase.order',
                    method: 'search_count',
                    args: [[['state', '=', 'draft']]],  // RFQ
                    kwargs: {}
                }),
                this.rpc('/web/dataset/call_kw', {
                    model: 'sale.order',
                    method: 'search_count',
                    args: [[['state', '=', 'draft']]],  // Quotations
                    kwargs: {}
                }),
                this.rpc('/web/dataset/call_kw', {
                    model: 'crm.lead',
                    method: 'search_count',
                    args: [[['type', '=', 'opportunity']]],  // Pipeline (Opportunities)
                    kwargs: {}
                }),
                this.rpc('/web/dataset/call_kw', {
                    model: 'crm.team',
                    method: 'search_count',
                    args: [[]],  // Fetch all teams
                    kwargs: {}
                })
            ]);

            // Update state with results
            this.state.sales_count = sales_result;
            this.state.leads_count = leads_result;
            this.state.invoice_count = invoices_result;
            this.state.bill_count = bills_result;
            this.state.customer_count = customers_result;
            this.state.vendor_count = vendors_result;
            this.state.purchase_count = purchase_result;
            this.state.rfq_count = rfq_result;
            this.state.quotation_count = quotation_result;
            this.state.pipeline_count = pipeline_result;
            this.state.sales_team_count = sales_team_result;
        });
    }

    _onClickTeam() {
        this.action.doAction({
            name: "Sales Team",
            type: 'ir.actions.act_window',
            res_model: 'sale.order',
            views: [[false, 'list'], [false, 'form']],
            domain: [['state', '=', 'sale']],  // Only confirmed Sales Orders
            context: {create: false, group_by: 'team_id'},
            target: 'current'
        });
    }


    _onClickSales() {
        this.action.doAction({
            name: "Sales Orders",
            type: 'ir.actions.act_window',
            res_model: 'sale.order',
            views: [[false, 'list'], [false, 'form']],
            domain: [['state', '=', 'sale']],  // Only confirmed Sales Orders
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
            domain: [['type', '=', 'lead']],
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

    _onClickCustomers() {
        this.action.doAction({
            name: "Customers",
            type: 'ir.actions.act_window',
            res_model: 'res.partner',
            views: [[false, 'list'], [false, 'form']],
            context: {create: false, search_default_customer: 1},
            domain: [['customer_rank', '>', 0]],
            target: 'current'
        });
    }

    _onClickVendors() {
        this.action.doAction({
            name: "Vendors",
            type: 'ir.actions.act_window',
            res_model: 'res.partner',
            views: [[false, 'list'], [false, 'form']],
            context: {create: false, search_default_supplier: 1},
            domain: [['supplier_rank', '>', 0]],
            target: 'current'
        });
    }

    _onClickPurchases() {
        this.action.doAction({
            name: "Purchase Orders",
            type: 'ir.actions.act_window',
            res_model: 'purchase.order',
            views: [[false, 'list'], [false, 'form']],
            domain: [['state', '=', 'purchase']],  // Only confirmed Purchase Orders
            context: {create: false},
            target: 'current'
        });
    }

    _onClickRFQ() {
        this.action.doAction({
            name: "Requests for Quotation",
            type: 'ir.actions.act_window',
            res_model: 'purchase.order',
            views: [[false, 'list'], [false, 'form']],
            domain: [['state', '=', 'draft']],
            target: 'current'
        });
    }

    _onClickQuotations() {
        this.action.doAction({
            name: "Quotations",
            type: 'ir.actions.act_window',
            res_model: 'sale.order',
            views: [[false, 'list'], [false, 'form']],
            domain: [['state', '=', 'draft']],
            target: 'current'
        });
    }

    _onClickPipeline() {
        this.action.doAction({
            name: "Pipeline",
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
            domain: [['type', '=', 'opportunity']],
            target: 'current'
        });
    }
}

ProjectDashboard.template = "ProjectDashBoardMain";
registry.category("actions").add("sales_dashboard_main", ProjectDashboard);
