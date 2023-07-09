import {css, CSSResultGroup, html, LitElement} from "lit";
import {HomeAssistant, Panel} from "custom-card-helpers";
import {customElement, property} from 'lit/decorators.js';
import './prog/prog'
import './ip/ip'
import './login/login'
import {HeatgerBackend} from "./api/heatger_backend";
import {VERSION} from "./consts";

@customElement('heatger-panel')
export class HeatgerPanel extends LitElement {
    @property() public hass!: HomeAssistant;
    @property() public panel!: Panel;
    @property({ type: Boolean, reflect: true }) public narrow!: boolean;
    @property() public connected: boolean = HeatgerBackend.isConnected();

    render() {
        return html`
            <div class="header">
                <div class="toolbar">
                    <ha-menu-button .hass=${this.hass} .narrow=${this.narrow}></ha-menu-button>
                    <div class="main-title">
                        Heatger
                    </div>
                    <div class="version">
                            v${VERSION}
                    </div>
                </div>
            </div>
            <div class="view">
                <div>
                ${this.getCards()}
                </div>
            </div>
        `;
    }

    reload(): void {
        this.requestUpdate();
    }

    getCards() {
        if(!HeatgerBackend.isConnected()) {
            return html`
                <heatger-login-card .hass=${this.hass} .narrow=${this.narrow} .panel=${this.panel} .reload="${this.reload.bind(this)}"></heatger-login-card>
            `;
        }
        return html`
            <heatger-prog-card .hass=${this.hass} .narrow=${this.narrow} .panel=${this.panel} .reload="${this.reload.bind(this)}"></heatger-prog-card>
            <heatger-ip-card .hass=${this.hass} .narrow=${this.narrow} .panel=${this.panel} .reload="${this.reload.bind(this)}"></heatger-ip-card>
        `;
    }

    static get styles(): CSSResultGroup {
        return css`
          .header {
            background-color: var(--app-header-background-color);
            color: var(--app-header-text-color, white);
            border-bottom: var(--app-header-border-bottom, none);
          }
          .toolbar {
            height: var(--header-height);
            display: flex;
            align-items: center;
            font-size: 20px;
            padding: 0 16px;
            font-weight: 400;
            box-sizing: border-box;
          }
          .main-title {
            margin: 0 0 0 24px;
            line-height: 20px;
            flex-grow: 1;
          }
          .version {
            font-size: 14px;
            font-weight: 500;
            color: rgba(var(--rgb-text-primary-color), 0.9);
          }
          .view {
            height: calc(100vh - 112px);
            display: flex;
            justify-content: center;
          }
          .view > * {
            width: 600px;
            max-width: 600px;
          }
          .view > *:last-child {
            margin-bottom: 20px;
          }
    `;
    }
}