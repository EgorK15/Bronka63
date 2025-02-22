// useMapData.ts
import { useState, useEffect, Dispatch, SetStateAction } from "react";
import { getObjects, getCategories } from "../services/mapServices";
import { Category, ObjectItem } from "@/utils/types";

function useMapData(date: string|null|undefined, setStartDate: Dispatch<SetStateAction<string|undefined>>, setStartTime: Dispatch<SetStateAction<string>>,time:string) {
  const [objects, setObjects] = useState<ObjectItem[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const fetchData = async () => {
    try {
      const objectsData = await getObjects();
      const categoriesData = await getCategories();
      // Add categoryName to each object
      objectsData.forEach((obj) => {
        obj.categoryName = categoriesData.find(
          (cat) => cat.id === obj.categoryId
        )?.name;
      });
      const somedate=new Date()
      setStartDate(somedate.toDateString());
      setStartTime("8:00");
      setObjects(objectsData);
      setCategories(categoriesData);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return { objects, categories, date,time,refetchData: fetchData };
}

export default useMapData;
