import {CSSResultGroup, html, LitElement} from "lit";
import {HomeAssistant, Panel} from "custom-card-helpers";
import {customElement, property, state} from 'lit/decorators.js';
import {getProgQuery} from "../api/prog/queries/get_prog_query";
import {Prog} from "../api/prog/dto/prog";
import './table_prog'
import {HeatgerProgTable} from "./table_prog";
import {deleteProgQuery} from "../api/prog/queries/delete_prog_query";
import {AxiosError} from "axios";
import {createProgQuery} from "../api/prog/queries/create_prog_query";
import {deleteAllProgQuery} from "../api/prog/queries/delete_all_prog_query";
import {localize} from "../../localize/localize";
import {style} from "../../style";

@customElement('heatger-prog-card')
export class HeatgerProgCard extends LitElement {
    @property() public hass!: HomeAssistant;
    @property() public panel!: Panel;
    @property({ type: Boolean, reflect: true }) public narrow!: boolean;
    @property() public reload!: () => void;
    @state() private error: string | null = null;
    @state() private currentTab: number = 0;

    firstUpdated() {
        this.switchTab(0)
    }

    switchTab(tab: number) {
        this.currentTab = tab;
        this.updateProgTable(getProgQuery(this.hass, tab+1))
    }

    handleAdd(event: MouseEvent) {
        const button = event.target as HTMLElement;
        button.blur();
        let form = this.shadowRoot!.querySelector('form');
        if(!form) return;
        const selectedDays: number[] = []
        const daysOptions = form['days'].options
        for(let i=0; i<daysOptions.length; i++) {
            if(daysOptions[i].selected) {
                selectedDays.push(i)
            }
        }
        const time = form['time'].value
        const state = parseInt(form['state'].value)
        const zone = parseInt(form['zone'].value)
        if(selectedDays.length === 0 || time === '') return;

        const progs: Prog[] = [];
        selectedDays.forEach((day) => {
            progs.push({day: day, hour: time, order: state});
        })
        this.updateProgTable(createProgQuery(this.hass, zone, progs));
    }

    handleDelete(prog: Prog) {
        this.updateProgTable(deleteProgQuery(this.hass, this.currentTab+1, prog))
    }

    handleDeleteAll(event: MouseEvent) {
        const button = event.target as HTMLElement;
        button.blur();
        this.updateProgTable(deleteAllProgQuery(this.hass, this.currentTab+1));
    }

    updateProgTable(query: Promise<Prog[]>) {
        this.error = null;
        const progTable = this.shadowRoot!.querySelector('heatger-prog-table') as HeatgerProgTable;
        if(!progTable) return;
        progTable.disabled = true;
        progTable.requestUpdate();
        query.then((r) => {
            progTable.datas = r;
            progTable.disabled = false;
            progTable.requestUpdate();
        }).catch((e: AxiosError) => {
            if(e.response && e.response.status === 401) {
                this.reload();
            }
            progTable.disabled = false;
            this.error = e.message;
            this.requestUpdate();
        });
    }

    render() {
        return html`
            <ha-card header="Prog">
                <div class="card-content">
                    <div class="content">
                        <form>
                            <div class="flexRow">
                                <label for="days">${localize('panel.prog.selectDays', this.hass.language)}</label>
                                <select name="days" id="days" multiple>
                                    <option value="0">${localize('dayOfWeek.monday', this.hass.language)}</option>
                                    <option value="1">${localize('dayOfWeek.tuesday', this.hass.language)}</option>
                                    <option value="2">${localize('dayOfWeek.wednesday', this.hass.language)}</option>
                                    <option value="3">${localize('dayOfWeek.thursday', this.hass.language)}</option>
                                    <option value="4">${localize('dayOfWeek.friday', this.hass.language)}</option>
                                    <option value="5">${localize('dayOfWeek.saturday', this.hass.language)}</option>
                                    <option value="6">${localize('dayOfWeek.sunday', this.hass.language)}</option>
                                </select>
                            </div>
                            <div class="flexRow">
                                <label for="time">${localize('panel.prog.setTime', this.hass.language)}</label>
                                <input type="time" name="time" id="time">
                            </div>
                            <div class="flexRow">
                                <label for="state">${localize('panel.prog.setState', this.hass.language)}</label>
                                <select name="state" id="state">
                                    <option value="0">${localize('state.comfort', this.hass.language)}</option>
                                    <option value="1">${localize('state.eco', this.hass.language)}</option>
                                </select>
                            </div>
                            <div class="flexRow">
                                <label for="zone">${localize('zone', this.hass.language)}</label>
                                <select name="zone" id="zone">
                                    <option value="1">${localize('zone', this.hass.language)} 1</option>
                                    <option value="2">${localize('zone', this.hass.language)} 2</option>
                                </select>
                            </div>
                            <div class="flexRow flexRow-center">
                                <mwc-button @click='${this.handleAdd}' class="button" id="add">
                                    ${localize('panel.add', this.hass.language)}
                                </mwc-button>
                                <mwc-button @click='${this.handleDeleteAll}' class="button" id="deleteAll">
                                    ${localize('panel.deleteAll', this.hass.language)}
                                </mwc-button>
                            </div>
                        </form>
                        
                        <mwc-tab-bar>
                            <mwc-tab label="${localize('zone', this.hass.language)} 1" 
                                     @click="${() => this.switchTab(0)}"></mwc-tab>
                            <mwc-tab label="${localize('zone', this.hass.language)} 2" 
                                     @click="${() => this.switchTab(1)}"></mwc-tab>
                        </mwc-tab-bar>
                        ${this.error}
                        <heatger-prog-table .hass="${this.hass}" .rowClicked="${this.handleDelete.bind(this)}"></heatger-prog-table>
                    </div>
                </div>
            </ha-card>
        `;
    }

    static get styles(): CSSResultGroup {
        return style;
    }
}