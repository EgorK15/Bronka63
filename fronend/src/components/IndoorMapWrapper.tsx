import React, { useContext, useState } from "react";
import { isMobile } from "react-device-detect";
import { TransformComponent, TransformWrapper } from "react-zoom-pan-pinch";
import { MapDataContext, NavigationContext } from "../pages/Map";
import "../styles/map.css";
import {
  MapDataContextType,
  NavigationContextType,
  ObjectItem,
} from "../utils/types";
import { MapBackground, Paths, Objects } from "./IndoorMap";

import Controls from "./MapControls";
import ObjectDetailsModal from "./Modals/ObjectDetailsModal";
import { navigateToObject } from "@/utils/navigationHelper";
import { toast } from "react-toastify";
import ObjectRect from "./IndoorMap/Objects";
import { time } from "console";

function IndoorMapWrapper(){
  const [modalOpen, setModalOpen] = useState(false);
  const [object, setObject] = useState<ObjectItem>({} as ObjectItem);
  const positionRadius = isMobile ? 10 : 8;
  const { navigation, setNavigation, isEditMode, setIsEditMode } = useContext(
    NavigationContext
  ) as NavigationContextType;
  const { objects } = useContext(MapDataContext) as MapDataContextType;
  const { date } = useContext(MapDataContext) as MapDataContextType;
  const { time } = useContext(MapDataContext) as MapDataContextType;
  async function handleObjectClick(e: React.MouseEvent<SVGPathElement>) {
    if (!isEditMode) {
      const targetId = (e.target as HTMLElement).id;
      const selectedObject = objects.find((obj) => obj.number === targetId&& obj.date===date&& obj.time===time);
      if (selectedObject?.id) {
        setObject(selectedObject);
        setModalOpen(true);
      } else {
        toast.error("Object not found");
      }
    }
  }
  const handlePositionClick = (e: React.MouseEvent<SVGPathElement>) => {
    if (isEditMode) {
      const vertexId = (e.target as HTMLElement).id;
      setNavigation({ start: vertexId });
      setIsEditMode(false);
    }
  };

  function handleNavigationClick() {
    setModalOpen(false);
    navigateToObject(object.number, navigation, setNavigation);
  }
  console.log(date)
  console.log((objects.find((obj) => obj.number === '203'))?.date)
  return (
    <div className="relative w-full h-full bg-white center">
      <ObjectDetailsModal
        open={modalOpen}
        object={object}
        onClose={() => setModalOpen((cur) => !cur)}
        objectNavigation={handleNavigationClick}
      />

      <TransformWrapper
        centerOnInit
        minScale={isMobile ? 0.4 : 1}
        doubleClick={{ mode: "reset" }}
        initialScale={isMobile ? 0.4 : 1}
        smooth={true}
        wheel={{ smoothStep: 0.01 }}
      >
        <TransformComponent wrapperClass="bg-white">
          <MapBackground>
            {/*Objects are the clickable areas on the map e.g. Rooms, Desks, ...*/}
            <ObjectRect
              handleObjectClick={handleObjectClick}
              className={
                isEditMode ? "" : "hover:cursor-pointer hover:opacity-50"
              }
              colour={(objects.find((obj) => obj.number === '203'&& obj.date===date&& obj.time===time)?.colour)}
              id="203"
              d="M100 791l139.848.003-1.024 114.297-139.619.503.795-114.803z"
            />
            <ObjectRect
              handleObjectClick={handleObjectClick}
              className={
                isEditMode ? "" : "hover:cursor-pointer hover:opacity-50"
              }
              colour={(objects.find((obj) => obj.number === '204'&& obj.date===date&& obj.time===time)?.colour)}
              id="204"
              d="M255 791l134.848.003-1.024 114.297-134.619.503.795-114.803z"
            />
            <ObjectRect
              handleObjectClick={handleObjectClick}
              className={
                isEditMode ? "" : "hover:cursor-pointer hover:opacity-50"
              }
              colour={(objects.find((obj) => obj.number === '205'&& obj.date===date&& obj.time===time)?.colour)}
              id="205"
              d="M385 791l83.253.333-2.042 115.252-83.443.698.232-116.283z"
            />
             <ObjectRect
              handleObjectClick={handleObjectClick}
              className={
                isEditMode ? "" : "hover:cursor-pointer hover:opacity-50"
              }
              colour={(objects.find((obj) => obj.number === '207'&& obj.date===date&& obj.time===time)?.colour)}
              id="207"
              d="M790.849 791.04l105.416.003-1.091 114.297-105.171.503.846-104.803z"
            />
            <ObjectRect
              handleObjectClick={handleObjectClick}
              className={
                isEditMode ? "" : "hover:cursor-pointer hover:opacity-50"
              }
              colour={(objects.find((obj) => obj.number === '208'&& obj.date===date&& obj.time===time)?.colour)}
              id="208"
              d="M1030.126 791.04l123.189.003-1.08 114.297-122.947.503.838-114.803z"
            />
            <ObjectRect
              handleObjectClick={handleObjectClick}
              className={
                isEditMode ? "" : "hover:cursor-pointer hover:opacity-50"
              }
              colour={(objects.find((obj) => obj.number === '209'&& obj.date===date&& obj.time===time)?.colour)}
              id="209"
              d="M1170.509 777.562l228 4.068-.193 165.675-228.283-.602.048-165.141z"
            />
            <ObjectRect
              handleObjectClick={handleObjectClick}
              className={
                isEditMode ? "" : "hover:cursor-pointer hover:opacity-50"
              }
              colour={(objects.find((obj) => obj.number === '202'&& obj.date===date&& obj.time===time)?.colour)}
              id="202"
              d="M100.509 721.562l75 1.068-.193 55.675-75.283-.602.048-55.141z"
            />
            <ObjectRect
              handleObjectClick={handleObjectClick}
              className={
                isEditMode ? "" : "hover:cursor-pointer hover:opacity-50"
              }
              colour="red"
              id="Туалет"
              d="M100.509 595.562l75 1.068-.193 125.675-75.283-.602.048-125.141z"
            />
            {/*Edges are the lines on the map aka the paths*/}
            <Paths />
            {/*Vertexes are the circles on the map aka the positions*/}
          </MapBackground>
        </TransformComponent>
        <Controls />
      </TransformWrapper>
    </div>
  );
}
export default IndoorMapWrapper;
