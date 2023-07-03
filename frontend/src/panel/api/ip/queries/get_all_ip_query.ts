import {HeatgerBackend} from "../../heatger_backend";
import {HomeAssistant} from "custom-card-helpers";
import {IpDto} from "../dto/ip_dto";


export async function getAllIpQuery(hass: HomeAssistant): Promise<IpDto[]> {
    const api = await HeatgerBackend.build(hass)
    return await api.get<IpDto[]>(`ip`).then(r => r.data);
}
