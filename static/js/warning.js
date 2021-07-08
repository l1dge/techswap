function WarningUndoItemDel(){
    if(confirm("Sure you want to delete? This will delete your item and cannot be undone!")){
      return true;
    } else {
      return false;
    }
  }

  function WarningUndoItemArc(){
    if(confirm("Sure you want to archive?")){
      return true;
    } else {
      return false;
    }
  }