import { useState } from 'react';

import { getJams } from './services/api/jamsAPI';

import Header from './components/layout/Header';
import FetchForm from './components/search/FetchForm';
import GJCLoader from './components/layout/GJCLoader';
import JamsGrid from './components/jams/JamsGrid';

export default function App() {
  const [fetchFormOpened, setFetchFormOpened] = useState(false);
  const [jams, setJams] = useState( []);
  const [fetchingJams, setFetchingJams] = useState(false);
  
  const onSearchLaunch = numberOfJamsToSearch => {
    setFetchingJams(true);

    getJams(numberOfJamsToSearch)
      .then(jamsFetched => {
        console.log(jamsFetched);
        setJams(jamsFetched);
      })
      .catch(_ => alert('An error occured. Please try again later.'))
      .finally(_ => setFetchingJams(false));
  }

  return (
    <>
      <Header onGetJamsButtonClick={() => setFetchFormOpened(true)} />
      <FetchForm 
        formOpened={fetchFormOpened}
        closeForm={() => setFetchFormOpened(false)}
        onSearchLaunch={onSearchLaunch} 
      />
      { fetchingJams ? <GJCLoader /> : <JamsGrid jams={jams} /> }
    </>
  )
}