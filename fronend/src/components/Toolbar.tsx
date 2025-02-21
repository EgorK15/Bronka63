import { NavigationContext } from "@/pages/Map";
import { NavigationContextType } from "@/utils/types";
import { useContext} from "react";
import { isDesktop } from "react-device-detect";
import DesktopRouteDetails from "./DesktopRouteDetails";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { Dispatch, SetStateAction } from 'react';
type Props = { startDate: Date; startTime:string;setStartDate: Dispatch<SetStateAction<Date>>;setStartTime: Dispatch<SetStateAction<string>>;setStringDate:Dispatch<SetStateAction<string|undefined>>;stringDate:string|undefined};
function Toolbar({startDate, setStartDate,startTime,setStartTime,setStringDate,stringDate}:Props) { 
  const Example = () => {
    return <DatePicker selected={startDate} onChange={(date) => {date && setStartDate(date);setStringDate(date?.toDateString())}} />;
  };
  const { navigation } = useContext(NavigationContext) as NavigationContextType;
  return (
    <div className="flex space-x-1 mb-4 h-12 relative">
      <Example/>
      <select name="time" id="cars" onChange={(e)=>{setStartTime(e.target.value)}}>
          <option value="8:00">8:00</option>
          <option value="11:30">11:30</option>
          <option value="13:30">13:30</option>
          <option value="15:15">15:15</option>
          <option value="17:00">17:00</option>
          <option value="18:45">18:45</option>
          <option value="20:25">20:25</option>
        </select>
        <div style={{
          'width':'50px',
            'height':'25px',
              'background': 'green'}}/>
        -СВОбодно
        <div style={{
          'width':'50px',
            'height':'25px',
              'background': 'red'}}/>
        -ЗАНЯТО
      {navigation.end && isDesktop && <DesktopRouteDetails />}
    </div>
  );
}

export default Toolbar;
