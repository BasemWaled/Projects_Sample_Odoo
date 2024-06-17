/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Playground extends Component {
    static template = "owl_playground.playground";
    
    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
    }
}



// /** @odoo-module **/

// import { Component, useState } from "@odoo/owl";

// export class Playground extends Component {
//     static template = "owl_playground.playground";

//     static template = "owl_playground.Counter";

//     setup() {
//         this.state = useState({ value: 0 });
//     }

//     increment() {
//         this.state.value++;
//     }
// }
