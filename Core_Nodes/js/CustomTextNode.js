import { LitElement, html } from 'lit-element';

class CustomTextNode extends LitElement {
    static get properties() {
        return {
            widget: { type: Object }
        };
    }

    constructor() {
        super();
        this.widget = {};
    }

    render() {
        return html`
            <pre><code>${this.widget.output}</code></pre>
        `;
    }

    update(changedProperties) {
        if (changedProperties.has('widget')) {
            this.widget = changedProperties.get('widget');
        }
        super.update(changedProperties);
    }
}

customElements.define('custom-text-node', CustomTextNode);