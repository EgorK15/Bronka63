import { CSSProperties } from "@mui/material/styles/createMixins";

interface ObjectsProps {
  handleObjectClick: (e: React.MouseEvent<SVGPathElement>) => void;
  className?: string;
  colour?:string;
}
interface ObjectProps {
  handleObjectClick: (e: React.MouseEvent<SVGPathElement>) => void;
  className?: string;
  colour?:string;
  id?:string;
  d?:string;
}
function ObjectRect({handleObjectClick, className,colour,d,id}: ObjectProps){
  return(
    <path
        id={id}
        className={`${className} object`}
        style={{fill:colour, fillOpacity:'1'}}
        d={d}
        onClick={handleObjectClick}
      />
  )
}
function Objects({ handleObjectClick, className}: ObjectsProps) {
  return (
    <g id="Objects">
      <path
        id="203"
        className={`${className} object`}
        style={{fill:'red', fillOpacity:'1'}}
        d="M100 791l139.848.003-1.024 114.297-139.619.503.795-114.803z"
        onClick={handleObjectClick}
      />
      <path
        id="204"
        className={`${className} object`}
        style={{fill:'green', fillOpacity:'1'}}
        d="M255 791l134.848.003-1.024 114.297-134.619.503.795-114.803z"
        onClick={handleObjectClick}
      />
      <path
        id="205"
        className={`${className} object`}
        style={{fill:'green', fillOpacity:'1'}}
        d="M385 791l83.253.333-2.042 115.252-83.443.698.232-116.283z"
        onClick={handleObjectClick}
      />
      <path
        id="208"
        className={`${className} object`}
        style={{fill:'red', fillOpacity:'1'}}
        d="M1030.126 791.04l123.189.003-1.08 114.297-122.947.503.838-114.803z"
        onClick={handleObjectClick}
      />
      <path
        id="207"
        className={`${className} object`}
        style={{fill:'green', fillOpacity:'1'}}
        d="M790.849 791.04l105.416.003-1.091 114.297-105.171.503.846-104.803z"
        onClick={handleObjectClick}
      />
      <path
        id="209"
        className={`${className} object`}
        d="M1170.509 777.562l228 4.068-.193 165.675-228.283-.602.048-165.141z"
        onClick={handleObjectClick}
      />
      <path
        id="202"
        className={`${className} object`}
        d="M100.509 721.562l75 1.068-.193 55.675-75.283-.602.048-55.141z"
        onClick={handleObjectClick}
      />
      <path
        id="Туалет"
        className={`${className} object`}
        d="M100.509 595.562l75 1.068-.193 125.675-75.283-.602.048-125.141z"
        onClick={handleObjectClick}
      />
    </g>
  );
}
export default ObjectRect;
//export default Objects;
