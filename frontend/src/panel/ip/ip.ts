import {css, CSSResultGroup, html, LitElement} from "lit";
import {HomeAssistant, Panel} from "custom-card-helpers";
import {customElement, property, state} from 'lit/decorators.js';
import './table_ip'
import {HeatgerIpTable} from "./table_ip";
import {AxiosError} from "axios";
import {IpDto} from "../api/ip/dto/ip_dto";
import {getAllIpQuery} from "../api/ip/queries/get_all_ip_query";
import {createIpQuery} from "../api/ip/queries/create_ip_query";
import {deleteIpQuery} from "../api/ip/queries/delete_ip_query";
import {localize} from "../../localize/localize";

@customElement('heatger-ip-card')
export class HeatgerIpCard extends LitElement {
    @property() public hass!: HomeAssistant;
    @property() public panel!: Panel;
    @property({ type: Boolean, reflect: true }) public narrow!: boolean;
    @property() public reload!: () => void;
    @state() private error: string | null = null;

    firstUpdated() {
        this.updateIpTable(getAllIpQuery(this.hass))
    }

    handleAdd(event: MouseEvent) {
        const button = event.target as HTMLElement;
        button.blur();
        let form = this.shadowRoot!.querySelector('form');
        if(!form) return;
        const name = form['ipName'].value;
        const ip = form['ip'].value;
        const ipSplitted = ip.split('.')
        if(ipSplitted.length !== 4) return;
        if(ipSplitted[0] <= 0 || ipSplitted[0] >= 254 || ipSplitted[1] <= 0 || ipSplitted[1] >= 254 ||
            ipSplitted[2] <= 0 || ipSplitted[2] >= 254 || ipSplitted[3] <= 0 || ipSplitted[3] >= 254) return;

        this.updateIpTable(createIpQuery(this.hass, {name: name, ip: ip}));
    }

    handleDelete(ip: IpDto) {
        this.updateIpTable(deleteIpQuery(this.hass, ip))
    }

    updateIpTable(query: Promise<IpDto[]>) {
        this.error = null;
        const ipTable = this.shadowRoot!.querySelector('heatger-ip-table') as HeatgerIpTable;
        if(!ipTable) return;
        ipTable.disabled = true;
        ipTable.requestUpdate();
        query.then((r) => {
            ipTable.datas = r;
            ipTable.disabled = false;
            ipTable.requestUpdate();
        }).catch((e: AxiosError) => {
            if(e.response && e.response.status === 401) {
                this.reload();
            }
            ipTable.disabled = false;
            this.error = e.message;
            this.requestUpdate();
        });
    }

    render() {
        return html`
            <ha-card header="Ip">
                <div class="card-content">
                    <div class="content">
                        <form>
                            <div class="row">
                                <label for="ipName">${localize('panel.ip.setName', this.hass.language)}</label>
                                <input type="text" name="ipName" id="ipName">
                            </div>
                            <div class="row">
                                <label for="ip">${localize('panel.ip.setIp', this.hass.language)}</label>
                                <input type="text" name="ip" id="ip">
                            </div>
                            <div class="row row-center">
                                <mwc-button @click='${this.handleAdd}' class="button" id="add">
                                    ${localize('panel.add', this.hass.language)}
                                </mwc-button>
                            </div>
                        </form>
                        ${this.error}
                        <heatger-ip-table .hass="${this.hass}" .rowClicked="${this.handleDelete.bind(this)}"></heatger-ip-table>
                    </div>
                </div>
            </ha-card>
        `;
    }

    static get styles(): CSSResultGroup {
        return css`
          ha-card {
            display: flex;
            flex-direction: column;
            margin: 5px;
            max-width: calc(100vw - 10px);
          }
          
          h2 {
            text-align: center;
          }
          
          form {
            display: flex;
            flex-direction: column;
          }
          
          label {
            width: 120px;
          }
          
          .row {
            display: flex;
            margin-bottom: 0.5rem;
            justify-content: center;
          }
          
          .row-center {
            justify-content: center;
          }

          select, input {
            background-color: var(--mdc-text-field-fill-color);
            flex-grow: 1;
            border: none;
            border-radius: 5px;
            padding: 5px;
          }
        `;
    }
}