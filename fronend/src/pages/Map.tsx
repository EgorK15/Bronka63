import IndoorMapWrapper from "@/components/IndoorMapWrapper";
import MobileRouteDetails from "@/components/MobileRouteDetails";
import Toolbar from "@/components/Toolbar";
import useMapData from "@/hooks/useMapData";
import { createContext, useEffect, useState } from "react";
import { isDesktop, isMobile } from "react-device-detect";
import { useSearchParams } from "react-router-dom";
import {
  MapDataContextType,
  Navigation,
  NavigationContextType,
} from "../utils/types";

export const NavigationContext = createContext<NavigationContextType | null>(
  null
);
export const MapDataContext = createContext<MapDataContextType | null>(null);
const someDate=new Date();
function Map() {
  const [time,setTime]=useState<string>("8:00");
  const [calenderdate, setCalenderDate] = useState<Date>(someDate);
  const [date, setStartDate] = useState<string|undefined>();
  let [searchParams, setSearchParams] = useSearchParams();
  const defaultPosition = "v35";
  const startPosition = searchParams.get("position") || defaultPosition;
  const [navigation, setNavigation] = useState<Navigation>({
    start: startPosition,
    end: "",
  });
  const [isEditMode, setIsEditMode] = useState<boolean>(false);
  const navigationValue: NavigationContextType = {
    navigation,
    setNavigation,
    isEditMode,
    setIsEditMode,
  };

  useEffect(() => {
    setSearchParams({ position: navigation.start });
  }, [navigation.start]);
  const mapData = useMapData(date,setStartDate,setTime,time);
  return (
    <MapDataContext.Provider value={mapData}>
      <NavigationContext.Provider value={navigationValue}>
        <div className="flex bg-gray-100 text-gray-800 relative overflow-hidden w-full h-screen">
          {isDesktop}
          <main
            onChange={()=>{setStartDate(calenderdate.toDateString());console.log(calenderdate.toDateString())}}
            className={`flex w-full ${isDesktop && "-ml-96"} justify-center flex-grow flex-col md:p-10 p-2 transition-all duration-150 ease-in lg:ml-0`}
          >
            <Toolbar startDate={calenderdate} setStartDate={setCalenderDate} startTime={time} setStartTime={setTime} setStringDate={setStartDate} stringDate={date}/>
            <div className="center w-full h-full">
              <IndoorMapWrapper />
            </div>
          </main>
          {navigation.end && isMobile && <MobileRouteDetails />}
        </div>
      </NavigationContext.Provider>
    </MapDataContext.Provider>
  );
}

export default Map;
