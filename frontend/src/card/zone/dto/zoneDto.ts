import {State} from "../../enum/state";
import {Mode} from "../../enum/mode";

export type ZoneDto = {
    id: string;
    name: string;
    state: State;
    mode: Mode;
    nextChange: Date;
    isPing: boolean;
}