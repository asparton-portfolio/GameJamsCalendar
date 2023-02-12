import { useState } from 'react';
import PropTypes from 'prop-types';

import { Modal, NumberInput, Button } from '@mantine/core';

export default function FetchForm({ formOpened, closeForm, onSearchLaunch }) {
  const [count, setCount] = useState(50);

  /**
   * Close modal, reset form and launch search.
   */
  const onFormSubmit = submitEvent => {
    submitEvent.preventDefault();
    submitEvent.stopPropagation();

    closeForm();
    setCount(50);
    onSearchLaunch(count);
  }  

  return (
    <Modal
      opened={formOpened}
      onClose={() => closeForm()}
      title='Search configuration'
    >
      <form onSubmit={onFormSubmit}>
        <NumberInput 
          value={count}
          min={1}
          max={200}
          label='Count'
          description='Number of Game Jams to search for'
          withAsterisk
          onChange={newValue => setCount(newValue)}
        />
        <Button type='submit' color='pink' mt='md'>
          Launch search
        </Button>
      </form>
    </Modal>
  )
}

FetchForm.propTypes = {
  formOpened: PropTypes.bool,
  closeForm: PropTypes.func,
  onSearchLaunch: PropTypes.func
}