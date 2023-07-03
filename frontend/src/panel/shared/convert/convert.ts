import {localize} from "../../../localize/localize";

export const dayToStr = (day: number, language: string) => {
    switch (day) {
        case 0: return localize('dayOfWeek.monday', language)
        case 1: return localize('dayOfWeek.tuesday', language)
        case 2: return localize('dayOfWeek.wednesday', language)
        case 3: return localize('dayOfWeek.thursday', language)
        case 4: return localize('dayOfWeek.friday', language)
        case 5: return localize('dayOfWeek.saturday', language)
        case 6: return localize('dayOfWeek.sunday', language)
        default: return localize('error', language)
    }
}

export const orderToStr = (order: number, language: string) => {
    switch (order) {
        case 0: return localize('state.comfort', language)
        case 1: return localize('state.eco', language)
        case 2: return localize('state.frostFree', language)
        default: return localize('error', language)
    }
}

export const progToNumber = (day: number, hour: string): number => {
    const splitedHour = hour.split(':');
    if(splitedHour.length >= 2) {
        return day * 100 + parseInt(splitedHour.at(0) ?? '') * 10 + parseInt(splitedHour.at(1) ?? '');
    }
    return -1;
}
