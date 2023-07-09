import {HeatgerBackend} from "../../heatger_backend";
import {HomeAssistant} from "custom-card-helpers";
import {Prog} from "../dto/prog";
import {progToNumber} from "../../../../utils/convert/convert";


export async function deleteProgQuery(hass: HomeAssistant, zoneNumber: number, prog: Prog): Promise<Prog[]> {
    const api = await HeatgerBackend.build(hass)
    const URL = `prog/zone${zoneNumber}/${progToNumber(prog.day, prog.hour)}`;
    return await api.delete<Prog[]>(URL).then(r => r.data);
}
